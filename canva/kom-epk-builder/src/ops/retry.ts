// Retry wrapper for Canva SDK calls that throw CanvaError { code: "rate_limited" }.
// Error codes come from node_modules/@canva/error/index.d.ts (ErrorCode union); the public
// errors page could not be fetched at any guessed URL on 2026-09-10 (see BUILD-REPORT.md).
import { CanvaError } from "@canva/error";

// 2026-09-11, live: addElementAtPoint has its own rate limit ("Add native element rate
// limit exceeded"); 126 calls in a row lost 3 elements at four retries topping out at 4 s.
export const BACKOFF_MS = [500, 1000, 2000, 4000, 8000, 16000];
export const MAX_TRIES = 7;
export const PACE_MS = 150; // pause between consecutive addElementAtPoint calls

// Scopes per https://www.canva.dev/docs/apps/configuring-scopes/ (read 2026-09-10):
// addPage/addElementAtPoint -> canva:design:content:write, upload -> canva:asset:private:write,
// getCurrentPageContext -> canva:design:content:read. The installed @canva/error typings carry
// two codes for this: missing_permission (scope not set in the app config) and permission_denied
// (scope not accepted); https://www.canva.dev/docs/apps/handling-errors/ documents insufficient
// scopes as permission_denied (Codex audit 2026-09-11, finding 4). Both get the hint.
export const MISSING_PERMISSION_HINT =
  "(enable canva:design:content:write, canva:asset:private:write and canva:design:content:read on the app's Scopes page in the Developer Portal, then reload)";
export const PERMISSION_CODES: readonly string[] = [
  "missing_permission",
  "permission_denied",
];

function withHint(code: unknown, message: unknown): string {
  const base = `${String(code)}: ${String(message)}`;
  return typeof code === "string" && PERMISSION_CODES.includes(code)
    ? `${base} ${MISSING_PERMISSION_HINT}`
    : base;
}

export function errorMessage(e: unknown): string {
  if (e instanceof CanvaError) {
    return withHint(e.code, e.message);
  }
  if (e && typeof e === "object" && "code" in e && "message" in e) {
    const o = e as { code: unknown; message: unknown };
    return withHint(o.code, o.message);
  }
  if (e instanceof Error) {
    return e.message;
  }
  return String(e);
}

export function isRateLimited(e: unknown): boolean {
  if (e instanceof CanvaError) {
    return e.code === "rate_limited";
  }
  return (
    !!e &&
    typeof e === "object" &&
    "code" in e &&
    (e as { code: unknown }).code === "rate_limited"
  );
}

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

export async function withRetry<T>(
  label: string,
  fn: () => Promise<T>,
  log: (msg: string) => void,
): Promise<T> {
  let attempt = 0;
  for (;;) {
    attempt += 1;
    try {
      return await fn();
    } catch (e) {
      if (isRateLimited(e) && attempt < MAX_TRIES) {
        const wait = BACKOFF_MS[attempt - 1] ?? 4000;
        log(
          `${label}: rate_limited, retry ${attempt}/${MAX_TRIES - 1} in ${wait} ms`,
        );
        await sleep(wait);
        continue;
      }
      throw e;
    }
  }
}
