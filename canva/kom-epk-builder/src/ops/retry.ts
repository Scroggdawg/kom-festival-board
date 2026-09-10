// Retry wrapper for Canva SDK calls that throw CanvaError { code: "rate_limited" }.
// Error codes come from node_modules/@canva/error/index.d.ts (ErrorCode union); the public
// errors page could not be fetched at any guessed URL on 2026-09-10 (see BUILD-REPORT.md).
import { CanvaError } from "@canva/error";

export const BACKOFF_MS = [500, 1000, 2000, 4000];
export const MAX_TRIES = 5;

// Scopes per https://www.canva.dev/docs/apps/configuring-scopes/ (read 2026-09-10):
// addPage/addElementAtPoint -> canva:design:content:write, upload -> canva:asset:private:write,
// getCurrentPageContext -> canva:design:content:read. A missing_permission error therefore
// almost always means one of those is off on the app's Scopes page in the Developer Portal.
export const MISSING_PERMISSION_HINT =
  "(enable canva:design:content:write, canva:asset:private:write and canva:design:content:read on the app's Scopes page in the Developer Portal, then reload)";

function withHint(code: unknown, message: unknown): string {
  const base = `${String(code)}: ${String(message)}`;
  return code === "missing_permission"
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
