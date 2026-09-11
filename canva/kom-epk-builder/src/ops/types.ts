// Data contract for canva/ops/epk-canva.json (schema 1), written by tools/build-epk-canva.py.
// All coordinates are pt in the 1296x1728 page space, y down from the page top.
// The app multiplies every coordinate by s = designPageWidthPx / page.width_pt.
//
// Beyond the brief's contract text, the emitter also writes on image elements
// (tools/build-epk-canva.py, image branch): `file` (repo-relative path of the JPEG) and
// `px` ([width, height] of the flattened JPEG in pixels). `px` is passed to upload() as the
// asset's own dimensions (review fix 2026-09-10); `file` is informational.

export type FontKey = string;

export type OpsFont = {
  family: string;
  weight: string; // Canva FontWeight name: normal | semibold | bold | ...
  fallback_family: string;
  fallback_weight: string;
};

export type OpsLink = { url: string; start: number; end: number };

export type OpsImage = {
  type: "image";
  url: string;
  x: number;
  y: number;
  w: number;
  h: number;
  alt?: string;
  file?: string; // repo-relative path of the derived JPEG (emitter extra, informational)
  px?: [number, number]; // true pixel size of the JPEG (emitter extra, used for upload())
};

export type OpsText = {
  type: "text";
  kind: "paragraph" | "line";
  text: string;
  font: FontKey;
  size_pt: number;
  leading_pt: number;
  /** paragraph only: the line count the kit measured in the contract's face */
  lines?: number;
  tracking_pt: number;
  color: string;
  align: "start" | "center" | "end" | "justify";
  x: number;
  y: number;
  w: number;
  links?: OpsLink[];
  // colour runs within the text (a key in DIM and its value in CREAM on one line); the whole
  // text takes `color` first, then each run overrides its range (emitter, 2026-09-11)
  runs?: { start: number; end: number; color: string }[];
};

export type OpsRule = {
  type: "rule";
  x: number;
  y: number;
  w: number;
  h: number;
  color: string;
};

export type OpsElement = OpsImage | OpsText | OpsRule;

export type OpsPage = {
  n: number;
  name: string;
  background: string;
  count?: number;
  elements: OpsElement[];
};

export type OpsDoc = {
  schema: number;
  generated: string;
  source: { kit_commit: string; epk_rev: number };
  page: { width_pt: number; height_pt: number };
  fonts: Record<FontKey, OpsFont>;
  pages: OpsPage[];
};

export function parseOps(raw: unknown): OpsDoc {
  if (!raw || typeof raw !== "object") {
    throw new Error("ops JSON is not an object");
  }
  const doc = raw as Partial<OpsDoc>;
  if (doc.schema !== 1) {
    throw new Error(`unsupported schema ${String(doc.schema)} (expected 1)`);
  }
  if (!doc.page || typeof doc.page.width_pt !== "number") {
    throw new Error("ops JSON missing page.width_pt");
  }
  if (typeof doc.page.height_pt !== "number") {
    throw new Error("ops JSON missing page.height_pt");
  }
  if (!Array.isArray(doc.pages)) {
    throw new Error("ops JSON missing pages[]");
  }
  if (!doc.fonts || typeof doc.fonts !== "object") {
    throw new Error("ops JSON missing fonts{}");
  }
  for (const p of doc.pages) {
    if (typeof p.n !== "number" || !Array.isArray(p.elements)) {
      throw new Error(
        `page entry malformed: ${JSON.stringify(p).slice(0, 80)}`,
      );
    }
    if (typeof p.count === "number" && p.count !== p.elements.length) {
      throw new Error(
        `page ${p.n}: count ${p.count} != elements.length ${p.elements.length}`,
      );
    }
  }
  return doc as OpsDoc;
}

export function countElements(doc: OpsDoc): number {
  return doc.pages.reduce((acc, p) => acc + p.elements.length, 0);
}
