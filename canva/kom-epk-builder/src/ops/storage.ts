// localStorage persistence: chosen font refs and per-page build progress so a reload resumes.
//
// Progress (review fix 2026-09-10): the record is namespaced by the ops file identity
// (`${generated}|${epk_rev}`) so a regenerated JSON never inherits a stale "done" list, and it
// keeps two maps — `done` (placed === attempted, zero failures; Build all skips these) and
// `failed` (anything else; Build all retries these). getDesignMetadata() carries no design id
// in the installed @canva/design 2.13.0 typings (title, defaultPageDimensions, pageMetadata,
// durationInSeconds only), so the design cannot be part of the key; README-APP.md tells the
// operator to Reset when switching designs.

export type StoredFont = {
  ref: string;
  name: string;
  weights: { weight: string; styles: string[] }[];
};

export type PageProgress = {
  n: number;
  name: string;
  elements_attempted: number;
  elements_placed: number;
  failures: string[];
  at: string; // ISO timestamp
  mode: "batch" | "per-element";
  page_id?: string; // PageMetadata.id returned by addPage (stable within the design)
  page_is_current?: boolean; // getCurrentPageMetadata().id === page_id right after addPage
};

export type ProgressRecord = {
  key: string; // `${doc.generated}|${doc.source.epk_rev}`
  done: Record<string, PageProgress>;
  failed: Record<string, PageProgress>;
};

const FONTS_KEY = "kom-epk-builder:fonts";
const PROGRESS_KEY = "kom-epk-builder:progress:v2";
const OPS_URL_KEY = "kom-epk-builder:ops_url";

export function progressKey(doc: {
  generated: string;
  source: { epk_rev: number };
}): string {
  return `${doc.generated}|${doc.source.epk_rev}`;
}

export function emptyProgress(key: string): ProgressRecord {
  return { key, done: {}, failed: {} };
}

function read<T>(key: string, fallback: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function write(key: string, value: unknown): void {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // storage unavailable; ignore (state is still in memory)
  }
}

export function loadFonts(): Record<string, StoredFont> {
  return read<Record<string, StoredFont>>(FONTS_KEY, {});
}

export function saveFonts(fonts: Record<string, StoredFont>): void {
  write(FONTS_KEY, fonts);
}

/** The persisted record, whatever ops file it belongs to; undefined when none. */
export function loadProgress(): ProgressRecord | undefined {
  const rec = read<ProgressRecord | undefined>(PROGRESS_KEY, undefined);
  if (!rec || typeof rec !== "object" || typeof rec.key !== "string") {
    return undefined;
  }
  return {
    key: rec.key,
    done: rec.done ?? {},
    failed: rec.failed ?? {},
  };
}

export function saveProgress(p: ProgressRecord): void {
  write(PROGRESS_KEY, p);
}

/** Record one page result: `done` when complete and clean, otherwise `failed`. */
export function recordPage(
  rec: ProgressRecord,
  page: PageProgress,
): ProgressRecord {
  const k = String(page.n);
  const { [k]: _d, ...done } = rec.done;
  const { [k]: _f, ...failed } = rec.failed;
  const clean =
    page.elements_placed === page.elements_attempted &&
    page.failures.length === 0;
  return clean
    ? { key: rec.key, done: { ...done, [k]: page }, failed }
    : { key: rec.key, done, failed: { ...failed, [k]: page } };
}

/** Drop one page from both maps so Build all will attempt it again. */
export function forgetPage(rec: ProgressRecord, n: number): ProgressRecord {
  const k = String(n);
  const { [k]: _d, ...done } = rec.done;
  const { [k]: _f, ...failed } = rec.failed;
  return { key: rec.key, done, failed };
}

export function clearProgress(): void {
  try {
    window.localStorage.removeItem(PROGRESS_KEY);
    window.localStorage.removeItem("kom-epk-builder:progress"); // pre-review key
  } catch {
    // ignore
  }
}

export function loadOpsUrl(fallback: string): string {
  return read<string>(OPS_URL_KEY, fallback);
}

export function saveOpsUrl(url: string): void {
  write(OPS_URL_KEY, url);
}
