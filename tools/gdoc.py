#!/usr/bin/env python3
"""Write a generated document straight into an existing Google Doc.

    gdoc.py auth                     one-time: print the consent URL, wait, store the token
    gdoc.py whoami                   confirm which account the stored token belongs to
    gdoc.py push <docId> <file.docx> replace that Doc's contents with the .docx
    gdoc.py backup <docId> <dir>     export the Doc as .docx and .txt before touching it

Why files.update and not the Docs API: replacing a Doc through documents().batchUpdate
means tearing the body down and rebuilding every run and its styling by hand, and any
mistake shows up as a silently mangled document. Drive's files.update takes the .docx
whole and lets Google do the conversion — the same thing File > Import > Replace does
in the UI. The Doc keeps its id, its URL and its sharing, which is the entire point:
Luke wants *that* document updated, not a new one beside it.

Credentials. The OAuth client is Luke's own ("bmf-agent", an installed-app client). It
is read from disk and never printed, never copied into the repository and never sent
anywhere but Google. The token is written to ~/.kom-gdoc/token.json with owner-only
permissions. The consent step happens in Luke's browser, under his own login — this
script never sees a password.

Scope is drive.file where possible, falling back to drive: Drive will not let an app
update a file it did not create unless it holds the broader scope, and the target Doc
was made by hand.
"""
import json, os, sys, glob, stat

HOME = os.path.expanduser("~")
CONF = os.path.join(HOME, ".kom-gdoc")
TOKEN = os.path.join(CONF, "token.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]
DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def client_secret_path():
    """The installed-app client, wherever Luke keeps it. Never read for printing."""
    env = os.environ.get("KOM_GDOC_CLIENT")
    if env and os.path.exists(env):
        return env
    here = os.path.join(CONF, "client_secret.json")
    if os.path.exists(here):
        return here
    found = sorted(glob.glob(os.path.join(HOME, "Downloads", "client_secret*.json")))
    if not found:
        sys.exit("no OAuth client found. Put one at ~/.kom-gdoc/client_secret.json "
                 "or set KOM_GDOC_CLIENT to its path.")
    return found[-1]


def _save(creds):
    os.makedirs(CONF, exist_ok=True)
    with open(TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN, stat.S_IRUSR | stat.S_IWUSR)      # owner only; it is a live credential


def credentials(interactive=False):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save(creds)
        return creds
    if not interactive:
        sys.exit("not authorised yet — run: gdoc.py auth")
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_path(), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=False,
                                  authorization_prompt_message="Open this URL to authorise:\n{url}\n",
                                  success_message="Authorised. You can close this tab.")
    _save(creds)
    return creds


def service(name, version):
    from googleapiclient.discovery import build
    return build(name, version, credentials=credentials(), cache_discovery=False)


def push(doc_id, path):
    """Replace the Doc's contents with this .docx, in place."""
    from googleapiclient.http import MediaFileUpload
    if not os.path.exists(path):
        sys.exit(f"no such file: {path}")
    drive = service("drive", "v3")
    before = drive.files().get(fileId=doc_id, fields="id,name,mimeType,modifiedTime").execute()
    if before["mimeType"] != "application/vnd.google-apps.document":
        sys.exit(f"{doc_id} is not a Google Doc ({before['mimeType']})")
    media = MediaFileUpload(path, mimetype=DOCX, resumable=False)
    after = drive.files().update(fileId=doc_id, media_body=media,
                                 fields="id,name,modifiedTime,webViewLink").execute()
    print(f"replaced {after['name']}")
    print(f"  was modified {before['modifiedTime']}")
    print(f"  now modified {after['modifiedTime']}")
    print(f"  {after['webViewLink']}")
    return after


def backup(doc_id, out_dir):
    """Export the Doc as it stands. Run before any push — the Doc is a place people
    type into, and a replace is not reversible from this side."""
    import io
    from googleapiclient.http import MediaIoBaseDownload
    os.makedirs(out_dir, exist_ok=True)
    drive = service("drive", "v3")
    meta = drive.files().get(fileId=doc_id, fields="name,modifiedTime").execute()
    stamp = meta["modifiedTime"].replace(":", "").replace("-", "")[:15]
    written = []
    for mime, ext in ((DOCX, "docx"), ("text/plain", "txt")):
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, drive.files().export_media(fileId=doc_id, mimeType=mime))
        done = False
        while not done:
            _, done = dl.next_chunk()
        path = os.path.join(out_dir, f"{meta['name']} {stamp}.{ext}")
        open(path, "wb").write(buf.getvalue())
        written.append(path)
    for w in written:
        print("saved", w)
    return written


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "auth":
        credentials(interactive=True)
        print("authorised; token stored at", TOKEN)
    elif cmd == "whoami":
        about = service("drive", "v3").about().get(fields="user").execute()
        print(about["user"].get("emailAddress"), "·", about["user"].get("displayName"))
    elif cmd == "backup":
        if len(a) < 3:
            sys.exit("usage: gdoc.py backup <docId> <dir>")
        backup(a[1], a[2])
    elif cmd == "push":
        if len(a) < 3:
            sys.exit("usage: gdoc.py push <docId> <file.docx>")
        push(a[1], a[2])
    else:
        sys.exit(f"unknown command {cmd}")


if __name__ == "__main__":
    main(sys.argv[1:])
