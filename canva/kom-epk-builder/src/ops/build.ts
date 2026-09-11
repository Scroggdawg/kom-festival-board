// Turns one OpsPage into Canva elements and adds it to the design.
//
// SDK calls used here and the docs read for each (2026-09-10):
//   addPage                https://www.canva.dev/docs/apps/api/design-add-page/
//   getCurrentPageMetadata https://www.canva.dev/docs/apps/api/design-get-current-page-metadata/
//   addElementAtPoint      https://www.canva.dev/docs/apps/api/design-add-element-at-point/
//   createRichtextRange    https://www.canva.dev/docs/apps/api/design-create-richtext-range/
//   upload                 https://www.canva.dev/docs/apps/api/asset-upload/
//   shape rectangle        https://www.canva.dev/docs/apps/creating-shapes/
// Type shapes were cross-checked against node_modules/@canva/design/index.d.ts and
// node_modules/@canva/asset/index.d.ts (the installed versions are the compile-time truth).
import type { FontRef, ImageMimeType, ImageRef } from "@canva/asset";
import { upload } from "@canva/asset";
import type {
  ElementAtPoint,
  FontWeight,
  ImageElementAtPoint,
  PageMetadata,
  RichtextElementAtPoint,
  ShapeElementAtPoint,
} from "@canva/design";
import {
  addElementAtPoint,
  addPage,
  createRichtextRange,
  getCurrentPageMetadata,
} from "@canva/design";
import { errorMessage, withRetry } from "./retry";
import type { StoredFont } from "./storage";
import type {
  OpsDoc,
  OpsElement,
  OpsImage,
  OpsPage,
  OpsRule,
  OpsText,
} from "./types";

export type Logger = (msg: string) => void;

export type BuildContext = {
  doc: OpsDoc;
  s: number; // px per pt
  fonts: Record<string, StoredFont>; // chosen refs keyed by font key
  libre?: StoredFont; // Libre Baskerville fallback (from findFonts or picker)
  log: Logger;
};

export type BuildResult = {
  n: number;
  name: string;
  attempted: number;
  placed: number;
  failures: string[];
  mode: "batch" | "per-element";
  page_id?: string; // PageMetadata.id from addPage (stable within the design)
  page_is_current?: boolean; // getCurrentPageMetadata().id === page_id right after addPage
};

const FONT_WEIGHTS: readonly FontWeight[] = [
  "normal",
  "thin",
  "extralight",
  "light",
  "medium",
  "semibold",
  "bold",
  "ultrabold",
  "heavy",
];

function asFontWeight(w: string): FontWeight | undefined {
  return (FONT_WEIGHTS as readonly string[]).includes(w)
    ? (w as FontWeight)
    : undefined;
}

const clamp = (v: number, lo: number, hi: number) =>
  Math.min(hi, Math.max(lo, v));

// Round to 3 dp: coordinates are pixels; avoids float noise in logs and payloads.
const px = (v: number) => Math.round(v * 1000) / 1000;

// Richtext `link` is documented only as "An external URL that the text links to"
// (https://www.canva.dev/docs/apps/api/design-create-richtext-range/); every example is https.
// mailto:/tel: are undocumented, so they are not sent (the text stays, the link is dropped).
export const HTTP_LINK = /^https?:\/\//i;

export function mimeFor(url: string): ImageMimeType {
  const path = url.split("?")[0]?.toLowerCase() ?? "";
  if (path.endsWith(".png")) {
    return "image/png";
  }
  if (path.endsWith(".webp")) {
    return "image/webp";
  }
  if (path.endsWith(".svg")) {
    return "image/svg+xml";
  }
  return "image/jpeg";
}

/** Resolve the font ref and weight for a text element's font key. */
export function resolveFont(
  ctx: BuildContext,
  key: string,
): { fontRef?: FontRef; fontWeight?: FontWeight; note?: string } {
  const spec = ctx.doc.fonts[key];
  const chosen = ctx.fonts[key];
  const wanted = spec?.weight ?? "normal";
  const fallbackWanted = spec?.fallback_weight ?? wanted;

  const pick = (
    font: StoredFont | undefined,
    weight: string,
  ): { fontRef: FontRef; fontWeight?: FontWeight } | undefined => {
    if (!font) {
      return undefined;
    }
    const has = font.weights.some((w) => w.weight === weight);
    const fw = asFontWeight(has ? weight : fallbackWanted);
    const hasFallback = font.weights.some((w) => w.weight === fallbackWanted);
    return {
      fontRef: font.ref as FontRef,
      fontWeight: has
        ? fw
        : hasFallback
          ? asFontWeight(fallbackWanted)
          : undefined,
    };
  };

  const primary = pick(chosen, wanted);
  if (primary) {
    return primary;
  }
  const fb = pick(ctx.libre, fallbackWanted);
  if (fb) {
    return {
      ...fb,
      note: `font ${key}: no chosen ref, using Libre Baskerville`,
    };
  }
  // No ref at all: fail the element rather than let Canva's default font in silently. Font
  // refs are short-lived per https://www.canva.dev/docs/apps/fonts/, so a ref stored by an
  // earlier session is not accepted either: the panel passes only refs resolved this session
  // (Codex audit 2026-09-11, finding 2).
  throw new Error(
    `font ${key}: no font ref resolved in this session (pick the font or find Libre Baskerville, then build)`,
  );
}

// --- element builders ---------------------------------------------------------

export async function uploadImage(
  ctx: BuildContext,
  el: OpsImage,
  label: string,
): Promise<ImageRef> {
  // upload(): https://www.canva.dev/docs/apps/api/asset-upload/
  // width/height ("A width, in pixels" / "A height, in pixels") are optional but must be given
  // together (AllOrNone<Dimensions>). They describe the asset, so the emitter's `px` (the
  // JPEG's true size) is used when present; the placement box is only the fallback.
  const width = el.px?.[0] ?? Math.round(el.w * ctx.s);
  const height = el.px?.[1] ?? Math.round(el.h * ctx.s);
  const queued = await withRetry(
    `${label} upload`,
    () =>
      upload({
        type: "image",
        mimeType: mimeFor(el.url),
        url: el.url,
        thumbnailUrl: el.url,
        aiDisclosure: "none",
        width,
        height,
      }),
    ctx.log,
  );
  // The ref may be used while the upload is in flight, but a delayed failure only surfaces
  // through whenUploaded(); awaiting it here means a page is never recorded complete with an
  // image that then fails (Codex audit 2026-09-11, finding 8).
  try {
    await queued.whenUploaded();
  } catch (e) {
    throw new Error(`${label}: upload did not complete: ${errorMessage(e)}`);
  }
  return queued.ref;
}

export function imageElement(
  ctx: BuildContext,
  el: OpsImage,
  ref: ImageRef,
): ImageElementAtPoint {
  // ImageElementAtPoint: https://www.canva.dev/docs/apps/api/design-add-element-at-point/
  return {
    type: "image",
    ref,
    altText: el.alt
      ? { text: el.alt, decorative: false }
      : { text: "", decorative: true },
    top: px(el.y * ctx.s),
    left: px(el.x * ctx.s),
    width: px(el.w * ctx.s),
    height: px(el.h * ctx.s),
  };
}

export function richtextElement(
  ctx: BuildContext,
  el: OpsText,
): { element: RichtextElementAtPoint; notes: string[] } {
  const notes: string[] = [];
  // createRichtextRange(): https://www.canva.dev/docs/apps/api/design-create-richtext-range/
  // "\n" marks a paragraph end, so appending the text with its newlines intact yields one
  // paragraph per line; a "\n\n" gap becomes an empty paragraph (visual blank line).
  const range = createRichtextRange();
  const { bounds } = range.appendText(el.text);
  const whole = { index: 0, length: bounds.length };

  const font = resolveFont(ctx, el.font);
  if (font.note) {
    notes.push(font.note);
  }

  const size = clamp(el.size_pt * ctx.s, 1, 1000);
  const lineHeightEm =
    el.size_pt > 0 ? clamp(el.leading_pt / el.size_pt, 0.5, 2.5) : 1.4;
  const letterSpacingEm =
    el.size_pt > 0 ? clamp(el.tracking_pt / el.size_pt, -0.2, 0.8) : 0;
  if (el.size_pt > 0 && el.tracking_pt / el.size_pt > 0.8) {
    notes.push(
      `tracking ${el.tracking_pt}pt on ${el.size_pt}pt exceeds 0.8em; clamped`,
    );
  }

  // fontRef / fontWeight are optional in the typings; only send the keys when a value exists
  // so no `undefined`-valued key crosses the iframe boundary (review fix 2026-09-10).
  range.formatParagraph(whole, {
    ...(font.fontRef ? { fontRef: font.fontRef } : {}),
    fontSize: px(size),
    textAlign: el.align,
    letterSpacingEm,
    lineHeightEm,
  });
  range.formatText(whole, {
    color: el.color,
    ...(font.fontWeight ? { fontWeight: font.fontWeight } : {}),
  });
  for (const link of el.links ?? []) {
    if (!HTTP_LINK.test(link.url)) {
      notes.push(
        `link ${link.url} skipped: non-http(s) scheme not documented for richtext links (text kept)`,
      );
      continue;
    }
    const start = clamp(link.start, 0, bounds.length);
    const end = clamp(link.end, start, bounds.length);
    if (end > start) {
      range.formatText(
        { index: start, length: end - start },
        { link: link.url },
      );
    } else {
      notes.push(
        `link ${link.url} has empty range [${link.start},${link.end})`,
      );
    }
  }

  // RichtextElementAtPoint = { type, range } & { top, left, width? } (no height; Canva wraps).
  return {
    element: {
      type: "richtext",
      range,
      top: px(el.y * ctx.s),
      left: px(el.x * ctx.s),
      width: px(el.w * ctx.s),
    },
    notes,
  };
}

/**
 * Rectangle shape: https://www.canva.dev/docs/apps/creating-shapes/
 * viewBox in the same units as width/height; path is the closed rectangle; fill colour, no
 * stroke. Height is the rule weight in pt scaled to px. `floor` raises sub-pixel heights to
 * 1 px; the docs state no minimum, so the exact height is tried first and the floored variant
 * only if Canva rejects the page (review fix 2026-09-10).
 */
export function ruleElement(
  ctx: BuildContext,
  el: OpsRule,
  floor = false,
): ShapeElementAtPoint {
  const w = Math.max(1, px(el.w * ctx.s));
  const exact = px(el.h * ctx.s);
  const h = floor ? Math.max(1, exact) : exact;
  return {
    type: "shape",
    paths: [
      {
        d: `M 0 0 H ${w} V ${h} H 0 L 0 0`,
        fill: { color: el.color },
      },
    ],
    viewBox: { top: 0, left: 0, width: w, height: h },
    top: px(el.y * ctx.s),
    left: px(el.x * ctx.s),
    width: w,
    height: h,
  };
}

function describe(el: OpsElement, i: number): string {
  if (el.type === "text") {
    return `#${i} text/${el.kind} "${el.text.slice(0, 24).replace(/\n/g, " ")}"`;
  }
  if (el.type === "image") {
    return `#${i} image ${el.url.split("/").pop() ?? el.url}`;
  }
  return `#${i} rule ${el.w}x${el.h}`;
}

// --- page builder ---------------------------------------------------------------

type Built = { el: ElementAtPoint; floored?: ElementAtPoint; label: string };

function pageIdOf(meta: PageMetadata): string | undefined {
  return meta.type === "absolute" ? meta.id : undefined;
}

/**
 * addPage() is documented as "Adds a new page immediately after the currently selected page"
 * and returns the new page's metadata (id is "Stable identifier for this page within the
 * design"). Whether the new page becomes the current page is NOT documented, so it is checked
 * at runtime: the returned id is compared with getCurrentPageMetadata().id.
 * Returns undefined when either id is unavailable (metadata type "unsupported" or id absent).
 */
async function checkCurrent(
  meta: PageMetadata,
  log: Logger,
  label: string,
): Promise<{ id?: string; isCurrent?: boolean }> {
  const id = pageIdOf(meta);
  try {
    const cur = await getCurrentPageMetadata();
    const curId = pageIdOf(cur);
    if (id === undefined || curId === undefined) {
      log(
        `${label}: page id ${id ?? "n/a"}, current page id ${curId ?? "n/a"} — cannot verify which page is current`,
      );
      return { id, isCurrent: undefined };
    }
    const isCurrent = id === curId;
    log(
      `${label}: page id ${id} ${isCurrent ? "is" : "is NOT"} the current page (current ${curId})`,
    );
    return { id, isCurrent };
  } catch (e) {
    log(`${label}: getCurrentPageMetadata failed: ${errorMessage(e)}`);
    return { id, isCurrent: undefined };
  }
}

export async function buildPage(
  ctx: BuildContext,
  page: OpsPage,
): Promise<BuildResult> {
  const { log, s } = ctx;
  const failures: string[] = [];
  const built: Built[] = [];
  const flooredRules: string[] = [];

  log(
    `page ${page.n} "${page.name}": preparing ${page.elements.length} elements (s=${s})`,
  );

  for (let i = 0; i < page.elements.length; i++) {
    const el = page.elements[i];
    if (!el) {
      continue;
    }
    const label = describe(el, i);
    try {
      if (el.type === "image") {
        const ref = await uploadImage(ctx, el, label);
        built.push({ el: imageElement(ctx, el, ref), label });
      } else if (el.type === "text") {
        const { element, notes } = richtextElement(ctx, el);
        notes.forEach((n) => log(`  ${label}: ${n}`));
        built.push({ el: element, label });
      } else if (el.type === "rule") {
        const exact = ruleElement(ctx, el, false);
        const floored = ruleElement(ctx, el, true);
        if (floored.height !== exact.height) {
          flooredRules.push(
            `${label} height floored ${exact.height} -> ${floored.height} px`,
          );
          built.push({ el: exact, floored, label });
        } else {
          built.push({ el: exact, label });
        }
      } else {
        failures.push(`${label}: unknown element type`);
      }
    } catch (e) {
      const msg = `${label}: prepare failed: ${errorMessage(e)}`;
      failures.push(msg);
      log(`  ${msg}`);
    }
  }

  const dims = {
    width: px(ctx.doc.page.width_pt * s),
    height: px(ctx.doc.page.height_pt * s),
  };
  const title = page.name.slice(0, 255);
  const base = {
    n: page.n,
    name: page.name,
    attempted: page.elements.length,
  };

  // Attempt 1: one addPage() with the whole batch, rules at exact height.
  // Attempt 1b (only when a rule is sub-pixel): the same batch with rules floored to 1 px.
  // addPage(): https://www.canva.dev/docs/apps/api/design-add-page/
  const batches: {
    label: string;
    elements: ElementAtPoint[];
    floored: boolean;
  }[] = [
    {
      label: "batch",
      elements: built.map((b) => b.el),
      floored: false,
    },
  ];
  if (flooredRules.length) {
    batches.push({
      label: "batch, rules floored",
      elements: built.map((b) => b.floored ?? b.el),
      floored: true,
    });
  }
  let lastBatchError = "";
  for (const batch of batches) {
    try {
      const meta = await withRetry(
        `page ${page.n} addPage(${batch.label})`,
        () =>
          addPage({
            title,
            dimensions: dims,
            background: { color: page.background },
            elements: batch.elements,
          }),
        log,
      );
      if (batch.floored) {
        flooredRules.forEach((m) => log(`  ${m}`));
      }
      const cur = await checkCurrent(meta, log, `page ${page.n}`);
      log(
        `page ${page.n}: addPage ${batch.label} ok — attempted ${page.elements.length}, placed ${built.length}, failures ${failures.length}`,
      );
      return {
        ...base,
        placed: built.length,
        failures,
        mode: "batch",
        page_id: cur.id,
        page_is_current: cur.isCurrent,
      };
    } catch (e) {
      lastBatchError = errorMessage(e);
      log(`page ${page.n}: addPage ${batch.label} rejected: ${lastBatchError}`);
    }
  }
  log(`page ${page.n}: falling back to per-element`);

  // Attempt 2: background-only page, then addElementAtPoint per element (rules floored).
  // addElementAtPoint(): https://www.canva.dev/docs/apps/api/design-add-element-at-point/
  // addElementAtPoint targets the current page, so placement only proceeds when the runtime
  // check confirms the new page is current; otherwise the elements would land on the wrong page.
  let meta: PageMetadata;
  try {
    meta = await withRetry(
      `page ${page.n} addPage(background)`,
      () =>
        addPage({
          title,
          dimensions: dims,
          background: { color: page.background },
        }),
      log,
    );
  } catch (e) {
    const msg = `page ${page.n}: addPage(background) failed: ${errorMessage(e)} (batch error was: ${lastBatchError})`;
    log(msg);
    failures.push(msg);
    return { ...base, placed: 0, failures, mode: "per-element" };
  }

  const cur = await checkCurrent(meta, log, `page ${page.n}`);
  if (cur.isCurrent === false) {
    const msg = `page ${page.n}: new page ${cur.id} is not the current page; per-element placement skipped — click that page in the editor, delete it, and press Build page ${page.n} again`;
    log(msg);
    failures.push(msg);
    return {
      ...base,
      placed: 0,
      failures,
      mode: "per-element",
      page_id: cur.id,
      page_is_current: false,
    };
  }
  if (cur.isCurrent === undefined) {
    log(
      `page ${page.n}: current-page check unavailable; placing per element on the current page anyway — verify with Read back`,
    );
  }

  if (flooredRules.length) {
    flooredRules.forEach((m) => log(`  ${m}`));
  }
  let placed = 0;
  for (const b of built) {
    const el = b.floored ?? b.el;
    try {
      await withRetry(
        `${b.label} addElementAtPoint`,
        () => addElementAtPoint(el),
        log,
      );
      placed += 1;
    } catch (e) {
      const msg = `${b.label}: addElementAtPoint failed: ${errorMessage(e)}`;
      failures.push(msg);
      log(`  ${msg}`);
    }
  }
  log(
    `page ${page.n}: per-element done — attempted ${page.elements.length}, placed ${placed}, failures ${failures.length}`,
  );
  return {
    ...base,
    placed,
    failures,
    mode: "per-element",
    page_id: cur.id,
    page_is_current: cur.isCurrent,
  };
}
