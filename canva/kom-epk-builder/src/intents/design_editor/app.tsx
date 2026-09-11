// KOM EPK Builder panel. Plain App UI Kit; every SDK call is wrapped in try/catch and
// logged to the panel. Only network call made by this code: the ops JSON fetch.
import { useFeatureSupport } from "@canva/app-hooks";
import {
  Alert,
  Button,
  FormField,
  MultilineInput,
  NumberInput,
  Rows,
  Text,
  TextInput,
  Title,
} from "@canva/app-ui-kit";
import type { Font } from "@canva/asset";
import { findFonts, requestFontSelection } from "@canva/asset";
import {
  addElementAtPoint,
  addPage,
  getCurrentPageContext,
  getDesignMetadata,
} from "@canva/design";
import type { CSSProperties } from "react";
import { useCallback, useEffect, useMemo, useState } from "react";
import * as styles from "styles/components.css";
import type { BuildContext } from "../../ops/build";
import { buildPage, placeOnCurrentPage } from "../../ops/build";
import type { ReadPage, WrapFlag } from "../../ops/readback";
import { flagWrapped, matchOpsPage, readBack } from "../../ops/readback";
import { errorMessage } from "../../ops/retry";
import type {
  PageProgress,
  ProgressRecord,
  StoredFont,
} from "../../ops/storage";
import {
  clearProgress,
  emptyProgress,
  forgetPage,
  loadFonts,
  loadOpsUrl,
  loadProgress,
  progressKey,
  recordPage,
  saveFonts,
  saveOpsUrl,
  saveProgress,
} from "../../ops/storage";
import type { OpsDoc } from "../../ops/types";
import { countElements, parseOps } from "../../ops/types";

export const APP_NAME = "kom-epk-builder";
export const DEFAULT_OPS_URL =
  "https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json";
const LIBRE_KEY = "__libre";
const LIBRE_NAME = "Libre Baskerville";

function toStored(font: Font): StoredFont {
  return {
    ref: font.ref,
    name: font.name,
    weights: font.weights.map((w) => ({
      weight: w.weight,
      styles: [...w.styles],
    })),
  };
}

export const App = () => {
  const isSupported = useFeatureSupport();
  const canAddPage = isSupported(addPage);
  const canAddElement = isSupported(addElementAtPoint);

  const [log, setLog] = useState<string[]>([]);
  const appendLog = useCallback((msg: string) => {
    const line = `${new Date().toISOString().slice(11, 19)} ${msg}`;
    setLog((prev) => [...prev.slice(-499), line]);
  }, []);

  // 1. Load operations
  const [opsUrl, setOpsUrl] = useState(() => loadOpsUrl(DEFAULT_OPS_URL));
  const [pasted, setPasted] = useState("");
  const [doc, setDoc] = useState<OpsDoc | undefined>();
  const [loadError, setLoadError] = useState<string | undefined>();

  const applyRaw = (raw: unknown, origin: string) => {
    try {
      const parsed = parseOps(raw);
      setDoc(parsed);
      setLoadError(undefined);
      appendLog(
        `loaded ops from ${origin}: schema ${parsed.schema}, generated ${parsed.generated}, epk_rev ${parsed.source.epk_rev}, ${parsed.pages.length} pages, ${countElements(parsed)} elements`,
      );
      // Progress is namespaced by ops identity; a record from another generated/epk_rev is
      // reported and not used for skipping (review fix 2026-09-10).
      const key = progressKey(parsed);
      const stored = loadProgress();
      if (stored && stored.key === key) {
        setProgress(stored);
        appendLog(
          `resume: ${Object.keys(stored.done).length} page(s) done, ${Object.keys(stored.failed).length} failed, for this ops file`,
        );
      } else {
        if (stored) {
          appendLog(
            `progress record is for ops "${stored.key}", loaded "${key}" — not used; Reset to discard it`,
          );
        }
        setProgress(emptyProgress(key));
      }
    } catch (e) {
      setLoadError(errorMessage(e));
      appendLog(`ops parse failed: ${errorMessage(e)}`);
    }
  };

  const onLoadUrl = async () => {
    saveOpsUrl(opsUrl);
    try {
      const res = await fetch(opsUrl, { cache: "no-store" });
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText}`);
      }
      applyRaw(await res.json(), opsUrl);
    } catch (e) {
      setLoadError(errorMessage(e));
      appendLog(`fetch failed: ${errorMessage(e)}`);
    }
  };

  const onLoadPasted = () => {
    try {
      applyRaw(JSON.parse(pasted), "pasted JSON");
    } catch (e) {
      setLoadError(errorMessage(e));
      appendLog(`pasted JSON invalid: ${errorMessage(e)}`);
    }
  };

  // 2. Probe: page size
  const [pagePx, setPagePx] = useState<
    | { source: string; width: number; height: number }
    | { source: string; width: undefined; height: undefined }
    | undefined
  >();
  const widthPt = doc?.page.width_pt ?? 1296;
  const s =
    pagePx && pagePx.width !== undefined ? pagePx.width / widthPt : undefined;

  const onProbePage = async () => {
    // getDesignMetadata(): https://www.canva.dev/docs/apps/api/design-get-design-metadata/
    // (exported from @canva/design, not @canva/platform — see BUILD-REPORT.md)
    try {
      const meta = await getDesignMetadata();
      const d = meta.defaultPageDimensions;
      if (d) {
        setPagePx({
          source: "getDesignMetadata().defaultPageDimensions",
          ...d,
        });
        appendLog(`page size (design metadata): ${d.width} x ${d.height} px`);
        return;
      }
      appendLog("getDesignMetadata().defaultPageDimensions is undefined");
    } catch (e) {
      appendLog(`getDesignMetadata failed: ${errorMessage(e)}`);
    }
    // getCurrentPageContext(): https://www.canva.dev/docs/apps/api/design-get-current-page-context/
    try {
      const ctx = await getCurrentPageContext();
      const d = ctx.dimensions;
      if (d) {
        setPagePx({ source: "getCurrentPageContext().dimensions", ...d });
        appendLog(
          `page size (current page context): ${d.width} x ${d.height} px`,
        );
        return;
      }
      appendLog(
        "getCurrentPageContext().dimensions is undefined (no fixed page size)",
      );
      setPagePx({
        source: "both probes undefined",
        width: undefined,
        height: undefined,
      });
    } catch (e) {
      appendLog(`getCurrentPageContext failed: ${errorMessage(e)}`);
      setPagePx({
        source: "both probes failed",
        width: undefined,
        height: undefined,
      });
    }
  };

  // A fresh Preview design has its own size; when the app cannot be opened inside the
  // 18 x 24 in poster, the operator types the target width and every page is added at that
  // width with the kit's 3:4 proportion (Codex audit 2026-09-11, finding 3). Whether Canva
  // honours addPage dimensions that differ from the design's default is undocumented; check
  // the first built page in Resize > Custom before building more.
  const [manualWidth, setManualWidth] = useState<number | undefined>();
  const onManualPage = () => {
    if (manualWidth === undefined || !doc) {
      appendLog("manual page size: load ops and enter a width first");
      return;
    }
    const height = Math.round(
      (manualWidth * doc.page.height_pt) / doc.page.width_pt,
    );
    setPagePx({ source: "manual override", width: manualWidth, height });
    appendLog(`page size (manual override): ${manualWidth} x ${height} px`);
  };

  // 3. Probe: fonts
  // Stored refs are shown for reference only: Canva documents font refs as short-lived
  // (https://www.canva.dev/docs/apps/fonts/), so a build uses only refs resolved in THIS panel
  // session (`fresh`). Codex audit 2026-09-11, finding 2.
  const [fonts, setFonts] = useState<Record<string, StoredFont>>(() =>
    loadFonts(),
  );
  const [fresh, setFresh] = useState<Set<string>>(() => new Set());
  const [libreMatches, setLibreMatches] = useState<StoredFont[]>([]);
  const fontKeys = useMemo(() => Object.keys(doc?.fonts ?? {}), [doc]);
  const fontsFresh =
    fontKeys.length > 0 && fontKeys.every((k) => fresh.has(k) && !!fonts[k]);
  const staleKeys = fontKeys.filter((k) => !!fonts[k] && !fresh.has(k));

  const storeFont = (key: string, font: StoredFont) => {
    setFonts((prev) => {
      const next = { ...prev, [key]: font };
      saveFonts(next);
      return next;
    });
    setFresh((prev) => new Set(prev).add(key));
  };

  const onPickFont = async (key: string) => {
    // requestFontSelection(): https://www.canva.dev/docs/apps/api/asset-request-font-selection/
    try {
      const current = fonts[key]?.ref;
      const res = await requestFontSelection(
        current ? { selectedFontRef: current as Font["ref"] } : undefined,
      );
      if (res.type === "completed") {
        storeFont(key, toStored(res.font));
        appendLog(
          `font ${key}: ${res.font.name} (${res.font.ref}) weights ${res.font.weights.map((w) => w.weight).join(",")}`,
        );
      } else {
        appendLog(`font ${key}: selection aborted`);
      }
    } catch (e) {
      appendLog(`requestFontSelection(${key}) failed: ${errorMessage(e)}`);
    }
  };

  const onFindLibre = async () => {
    // findFonts(): https://www.canva.dev/docs/apps/api/asset-find-fonts/
    try {
      const res = await findFonts();
      const matches = res.fonts
        .filter((f) => f.name.toLowerCase().includes(LIBRE_NAME.toLowerCase()))
        .map(toStored);
      setLibreMatches(matches);
      appendLog(
        `findFonts: ${res.fonts.length} fonts total, ${matches.length} matching "${LIBRE_NAME}"`,
      );
      const first = matches[0];
      if (first) {
        storeFont(LIBRE_KEY, first);
        appendLog(`Libre fallback set: ${first.name} (${first.ref})`);
      }
    } catch (e) {
      appendLog(`findFonts failed: ${errorMessage(e)}`);
    }
  };

  // 4. Build
  const [progress, setProgress] = useState<ProgressRecord>(() =>
    emptyProgress(""),
  );
  const [pageN, setPageN] = useState<number | undefined>(1);
  // Observed 2026-09-11 on the full build: each addPage() lands AFTER the previously added
  // page (the insertion point follows the new page) even though getCurrentPageMetadata()
  // reports the new page as not current. Ascending order therefore reads in order; a
  // reverse run (tried first, on the strength of that reading) came out backwards.
  const [reverseOrder, setReverseOrder] = useState(false);
  const [building, setBuilding] = useState(false);
  const [lastError, setLastError] = useState<string | undefined>();

  useEffect(() => {
    // mount-time notice only; reads the persisted record directly so the effect has no deps
    const stored = loadProgress();
    if (stored) {
      appendLog(
        `resume: localStorage holds progress for ops "${stored.key}" (${Object.keys(stored.done).length} done, ${Object.keys(stored.failed).length} failed); it applies once that ops file is loaded`,
      );
    }
  }, [appendLog]);

  const commitProgress = (next: ProgressRecord) => {
    saveProgress(next);
    setProgress(next);
  };

  const makeCtx = (): BuildContext | undefined => {
    if (!doc) {
      appendLog("build: load ops first");
      return undefined;
    }
    if (s === undefined) {
      appendLog("build: probe page size first (s is undefined)");
      return undefined;
    }
    if (!fontsFresh) {
      appendLog(
        `build: pick every font in this session first (${fontKeys.filter((k) => !fresh.has(k)).join(", ") || "none listed"}); refs stored by an earlier session are not used`,
      );
      return undefined;
    }
    const sessionFonts: Record<string, StoredFont> = {};
    for (const k of fontKeys) {
      const f = fonts[k];
      if (f && fresh.has(k)) {
        sessionFonts[k] = f;
      }
    }
    return {
      doc,
      s,
      fonts: sessionFonts,
      libre: fresh.has(LIBRE_KEY) ? fonts[LIBRE_KEY] : undefined,
      log: appendLog,
    };
  };

  const runPages = async (ns: number[], onCurrent = false) => {
    const ctx = makeCtx();
    if (!ctx) {
      return;
    }
    setBuilding(true);
    try {
      for (const n of ns) {
        const page = ctx.doc.pages.find((p) => p.n === n);
        if (!page) {
          appendLog(`page ${n}: not in ops JSON`);
          continue;
        }
        try {
          const r = onCurrent
            ? await placeOnCurrentPage(ctx, page)
            : await buildPage(ctx, page);
          const rec: PageProgress = {
            n: r.n,
            name: r.name,
            elements_attempted: r.attempted,
            elements_placed: r.placed,
            failures: r.failures,
            at: new Date().toISOString(),
            mode: r.mode,
            page_id: r.page_id,
            page_is_current: r.page_is_current,
          };
          setProgress((prev) => {
            const next = recordPage(prev, rec);
            saveProgress(next);
            return next;
          });
          if (r.failures.length) {
            setLastError(r.failures[r.failures.length - 1]);
          }
        } catch (e) {
          const msg = `page ${n}: unhandled: ${errorMessage(e)}`;
          appendLog(msg);
          setLastError(msg);
        }
      }
    } finally {
      setBuilding(false);
    }
  };

  const onBuildOne = () => {
    if (pageN === undefined) {
      appendLog("build: enter a page number");
      return;
    }
    void runPages([pageN]);
  };

  const onPlaceCurrent = () => {
    if (pageN === undefined) {
      appendLog("place: enter a page number");
      return;
    }
    void runPages([pageN], true);
  };

  const onBuildAll = () => {
    if (!doc) {
      appendLog("build: load ops first");
      return;
    }
    // Only clean pages (placed === attempted, no failures) are skipped; failed ones are retried.
    const remaining = doc.pages
      .map((p) => p.n)
      .filter((n) => !progress.done[String(n)]);
    if (reverseOrder) {
      remaining.reverse();
    }
    const retry = remaining.filter((n) => progress.failed[String(n)]);
    appendLog(
      `build all: ${remaining.length} of ${doc.pages.length} pages remaining, order ${remaining.join(",")} (${retry.length} recorded as failed will be retried — delete their partial pages in the editor first)`,
    );
    void runPages(remaining);
  };

  const onResetProgress = () => {
    clearProgress();
    setProgress(emptyProgress(doc ? progressKey(doc) : ""));
    appendLog("progress cleared");
  };

  const onForgetPage = (n: number) => {
    commitProgress(forgetPage(progress, n));
    appendLog(`page ${n}: progress record forgotten`);
  };

  const progressRows = [
    ...Object.values(progress.done).map((p) => ({ p, status: "done" })),
    ...Object.values(progress.failed).map((p) => ({ p, status: "FAILED" })),
  ].sort((a, b) => a.p.n - b.p.n);

  // 5. Export STATE
  const [stateJson, setStateJson] = useState("");
  // Emits the same subtree shape as canva/STATE.json so the block merges without hand
  // translation (review fix 2026-09-10): probes.page_size, probes.fonts.<key>, design.page_px,
  // design.scale_px_per_pt, ops.epk_rev_built_from, pages_built[], last_error.
  const onExportState = () => {
    const fontOut = (f: StoredFont | undefined) =>
      f
        ? { ref: f.ref, name: f.name, weights: f.weights.map((w) => w.weight) }
        : null;
    const fontsOut: Record<string, unknown> = {
      done: fontKeys.length > 0 && fontKeys.every((k) => !!fonts[k]),
      resolved_this_session: fontsFresh,
    };
    for (const k of fontKeys) {
      fontsOut[k] = fontOut(fonts[k]);
    }
    fontsOut["Libre Baskerville"] = fontOut(fonts[LIBRE_KEY]);
    const havePx = !!pagePx && pagePx.width !== undefined;
    const state = {
      app: { name: APP_NAME },
      probes: {
        page_size: {
          done: havePx,
          width_px: havePx ? pagePx.width : null,
          height_px: havePx ? pagePx.height : null,
          source: pagePx?.source ?? null,
        },
        fonts: fontsOut,
      },
      design: {
        url: null, // not readable by the app: copy it from the editor's address bar
        page_px: havePx ? [pagePx.width, pagePx.height] : null,
        scale_px_per_pt: s ?? null,
      },
      ops: {
        epk_rev_built_from: doc?.source.epk_rev ?? null,
        generated: doc?.generated ?? null,
        kit_commit: doc?.source.kit_commit ?? null,
      },
      pages_built: progressRows.map(({ p, status }) => ({
        n: p.n,
        name: p.name,
        status,
        elements_attempted: p.elements_attempted,
        elements_placed: p.elements_placed,
        mode: p.mode,
        failures: p.failures,
        page_id: p.page_id ?? null,
        page_is_current: p.page_is_current ?? null,
        at: p.at,
      })),
      last_error: lastError ?? null,
    };
    setStateJson(JSON.stringify(state, null, 2));
  };

  // 6. Read back
  const [readPages, setReadPages] = useState<ReadPage[] | undefined>();
  const [wrapFlags, setWrapFlags] = useState<WrapFlag[] | undefined>();
  const onReadBack = async () => {
    try {
      const r = await readBack(appendLog);
      setReadPages(r.pages);
      appendLog(
        `read back (${r.scope}): ${r.pages.map((p) => `p${p.index + 1}=${p.count}`).join(" ")}`,
      );
      // Wrap check: pair each read page with an ops page (by position when the read covers
      // every page, else unique element-count match, else the Page n field) and flag `line`
      // elements taller than leading*s*1.3 and paragraphs longer than their measured lines.
      if (doc && s !== undefined) {
        const flags: WrapFlag[] = [];
        for (const rp of r.pages) {
          const ops = matchOpsPage(doc, rp, pageN, r.pages.length);
          if (!ops) {
            appendLog(
              `wrap check: read page ${rp.index + 1} (${rp.count} elements) matches no ops page by count; set Page n and read again`,
            );
            continue;
          }
          const f = flagWrapped(ops, rp, s);
          appendLog(
            `wrap check: read page ${rp.index + 1} = ops page ${ops.n}, ${f.length} WRAPPED line(s)`,
          );
          flags.push(...f);
        }
        setWrapFlags(flags);
      } else {
        setWrapFlags(undefined);
        appendLog("wrap check skipped: load ops and probe page size first");
      }
    } catch (e) {
      appendLog(`read back failed: ${errorMessage(e)}`);
    }
  };

  const mono: CSSProperties = {
    fontFamily: "monospace",
    fontSize: 11,
    whiteSpace: "pre-wrap",
    wordBreak: "break-all",
    maxHeight: 220,
    overflow: "auto",
    margin: 0,
  };

  return (
    <div className={styles.scrollContainer}>
      <Rows spacing="2u">
        <Title size="small">KOM EPK Builder</Title>
        {!canAddPage && (
          <Alert tone="warn">
            addPage is not supported on this design surface.
          </Alert>
        )}
        {!canAddElement && (
          <Alert tone="warn">
            addElementAtPoint is not supported on this page.
          </Alert>
        )}

        <Title size="xsmall">1. Load operations</Title>
        <FormField
          label="Ops JSON URL"
          value={opsUrl}
          control={(props) => (
            <TextInput {...props} type="url" onChange={setOpsUrl} />
          )}
        />
        <Button variant="primary" onClick={() => void onLoadUrl()}>
          Load
        </Button>
        <FormField
          label="Or paste JSON"
          value={pasted}
          control={(props) => (
            <MultilineInput
              {...props}
              minRows={3}
              maxRows={6}
              onChange={setPasted}
            />
          )}
        />
        <Button
          variant="secondary"
          onClick={onLoadPasted}
          disabled={!pasted.trim()}
        >
          Use pasted JSON
        </Button>
        {loadError && <Alert tone="critical">{loadError}</Alert>}
        {doc && (
          <Text size="small">
            schema {doc.schema} · generated {doc.generated} · epk_rev{" "}
            {doc.source.epk_rev} · {doc.pages.length} pages ·{" "}
            {countElements(doc)} elements · kit{" "}
            {doc.source.kit_commit.slice(0, 8)}
          </Text>
        )}

        <Title size="xsmall">2. Probe: page size</Title>
        <Button variant="secondary" onClick={() => void onProbePage()}>
          Read page size
        </Button>
        {pagePx && (
          <Text size="small">
            {pagePx.width === undefined
              ? `page px: undefined (${pagePx.source})`
              : `page px: ${pagePx.width} x ${pagePx.height} (${pagePx.source}) · width_pt ${widthPt} · s = ${s?.toFixed(6)}`}
          </Text>
        )}
        <FormField
          label="Or type the page width in px (fresh design only; unverified)"
          value={manualWidth}
          control={(props) => (
            <NumberInput
              {...props}
              min={40}
              max={8000}
              step={1}
              onChange={(v) => setManualWidth(v)}
            />
          )}
        />
        <Button
          variant="tertiary"
          onClick={onManualPage}
          disabled={manualWidth === undefined || !doc}
        >
          Use this width
        </Button>

        <Title size="xsmall">3. Probe: fonts</Title>
        {fontKeys.length === 0 && (
          <Text size="small">Load ops to list font keys.</Text>
        )}
        {fontKeys.map((key) => {
          const spec = doc?.fonts[key];
          const chosen = fonts[key];
          return (
            <Rows key={key} spacing="0.5u">
              <Button variant="secondary" onClick={() => void onPickFont(key)}>
                {`Pick font for ${key} (${spec?.family ?? "?"} ${spec?.weight ?? ""})`}
              </Button>
              <Text size="xsmall">
                {chosen
                  ? `${chosen.name} · ${chosen.ref} · ${chosen.weights.map((w) => w.weight).join(",")} · ${fresh.has(key) ? "resolved this session" : "stored earlier, stale: pick again before building"}`
                  : "not chosen"}
              </Text>
            </Rows>
          );
        })}
        {staleKeys.length > 0 && (
          <Alert tone="warn">
            {`${staleKeys.length} font ref(s) come from an earlier session and will not be used: ${staleKeys.join(", ")}. Pick each again; Build enables when every key is resolved here.`}
          </Alert>
        )}
        <Button variant="secondary" onClick={() => void onFindLibre()}>
          Find Libre Baskerville
        </Button>
        {libreMatches.map((f) => (
          <Text key={f.ref} size="xsmall">
            {`${f.name} · ${f.ref} · ${f.weights.map((w) => w.weight).join(",")}`}
          </Text>
        ))}
        {fonts[LIBRE_KEY] && (
          <Text size="xsmall">{`fallback: ${fonts[LIBRE_KEY].name} · ${fonts[LIBRE_KEY].ref}`}</Text>
        )}

        <Title size="xsmall">4. Build</Title>
        <FormField
          label="Page n"
          value={pageN}
          control={(props) => (
            <NumberInput
              {...props}
              min={1}
              step={1}
              onChange={(v) => setPageN(v)}
            />
          )}
        />
        <Button
          variant="primary"
          onClick={onBuildOne}
          disabled={
            building || !doc || s === undefined || !canAddPage || !fontsFresh
          }
          loading={building}
        >
          Build page N
        </Button>
        <Button
          variant="secondary"
          onClick={onPlaceCurrent}
          disabled={
            building || !doc || s === undefined || !canAddElement || !fontsFresh
          }
        >
          Place page N on the current page (select it first; no addPage)
        </Button>
        <Button
          variant="secondary"
          onClick={onBuildAll}
          disabled={
            building || !doc || s === undefined || !canAddPage || !fontsFresh
          }
        >
          Build all pages (skips recorded)
        </Button>
        <Button
          variant="tertiary"
          onClick={() => setReverseOrder((v) => !v)}
          disabled={building}
        >
          {reverseOrder
            ? "Order: last page first (new pages land after the current page)"
            : "Order: first page first"}
        </Button>
        <Button
          variant="tertiary"
          onClick={onResetProgress}
          disabled={building}
        >
          Reset progress record
        </Button>
        {progressRows.map(({ p, status }) => (
          <Rows key={p.n} spacing="0.5u">
            <Text size="xsmall">
              {`page ${p.n} ${status}: ${p.elements_placed}/${p.elements_attempted} placed (${p.mode}) ${p.failures.length ? `· ${p.failures.length} failures` : ""} · id ${p.page_id ?? "n/a"} · current ${p.page_is_current === undefined ? "n/a" : String(p.page_is_current)} · ${p.at}`}
            </Text>
            <Button
              variant="tertiary"
              onClick={() => onForgetPage(p.n)}
              disabled={building}
            >
              {`Forget page ${p.n}`}
            </Button>
          </Rows>
        ))}

        <Title size="xsmall">5. Export STATE</Title>
        <Button variant="secondary" onClick={onExportState}>
          Render STATE JSON
        </Button>
        {stateJson && <pre style={mono}>{stateJson}</pre>}

        <Title size="xsmall">6. Read back</Title>
        <Button variant="secondary" onClick={() => void onReadBack()}>
          Read design (openDesign)
        </Button>
        {wrapFlags && wrapFlags.length > 0 && (
          <Alert tone="warn">
            {`${wrapFlags.length} WRAPPED line(s): ${wrapFlags.map((f) => `p${f.page_n}#${f.index} "${f.text}" ${f.read_px}px > ${f.expected_px}px`).join("; ")} — widen w in the emitter`}
          </Alert>
        )}
        {wrapFlags && wrapFlags.length === 0 && (
          <Text size="xsmall">wrap check: no wrapped lines</Text>
        )}
        {readPages && (
          <pre style={mono}>{JSON.stringify(readPages, null, 1)}</pre>
        )}

        <Title size="xsmall">Log</Title>
        <Button variant="tertiary" onClick={() => setLog([])}>
          Clear log
        </Button>
        <pre style={mono}>{log.join("\n")}</pre>
      </Rows>
    </div>
  );
};
