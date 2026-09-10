// Read-back of the current design for diffing against the ops JSON.
// openDesign(): https://www.canva.dev/docs/apps/api/design-open-design/ and
// https://www.canva.dev/docs/apps/design-editing/ (all_pages is documented as preview;
// the app tries it first and falls back to current_page). Session shapes taken from
// node_modules/@canva/design/index.d.ts (DesignEditing.AllPagesSession, CurrentPageSession).
import type { DesignEditing } from "@canva/design";
import { openDesign } from "@canva/design";
import { errorMessage } from "./retry";

export type ReadElement = {
  type: string;
  top: number;
  left: number;
  width: number;
  height: number;
};

export type ReadPage = {
  index: number;
  type: string;
  dimensions?: { width: number; height: number };
  count: number;
  elements: ReadElement[];
};

function snapshot(page: DesignEditing.Page, index: number): ReadPage {
  if (page.type !== "absolute") {
    return { index, type: page.type, count: 0, elements: [] };
  }
  const elements = page.elements.toArray().map((el) => ({
    type: el.type,
    top: Math.round(el.top * 100) / 100,
    left: Math.round(el.left * 100) / 100,
    width: Math.round(el.width * 100) / 100,
    height: Math.round(el.height * 100) / 100,
  }));
  return {
    index,
    type: page.type,
    dimensions: page.dimensions
      ? { width: page.dimensions.width, height: page.dimensions.height }
      : undefined,
    count: elements.length,
    elements,
  };
}

export async function readBack(
  log: (m: string) => void,
): Promise<{ scope: "all_pages" | "current_page"; pages: ReadPage[] }> {
  const pages: ReadPage[] = [];
  try {
    await openDesign({ type: "all_pages" }, async (session) => {
      const refs = session.pageRefs.toArray();
      log(`read back: all_pages session, ${refs.length} page refs`);
      let i = 0;
      for (const ref of refs) {
        const idx = i++;
        const res = await session.helpers.openPage(ref, async ({ page }) => {
          pages.push(snapshot(page, idx));
        });
        if (res.status === "skipped") {
          log(`read back: page ${idx + 1} skipped: ${res.reason}`);
          pages.push({ index: idx, type: "skipped", count: 0, elements: [] });
        }
      }
      // read-only: no session.sync()
    });
    return { scope: "all_pages", pages };
  } catch (e) {
    log(
      `read back: all_pages failed (${errorMessage(e)}); trying current_page`,
    );
  }
  await openDesign({ type: "current_page" }, async (session) => {
    pages.push(snapshot(session.page, 0));
    // read-only: no session.sync()
  });
  return { scope: "current_page", pages };
}

// --- wrap check (review fix 2026-09-10) -------------------------------------------
// The contract's `line` kind must not wrap, but the SDK has no no-wrap option; the emitter's
// slack was measured with macOS Baskerville while Canva renders Libre Baskerville. A wrapped
// line shows up in read-back as a richtext element roughly twice its leading tall.

import type { OpsDoc, OpsPage } from "./types";

export const WRAP_FACTOR = 1.3;

export type WrapFlag = {
  page_n: number;
  index: number; // element index within the page (z-order)
  text: string;
  expected_px: number; // leading_pt * s
  read_px: number;
};

/** Pick the ops page a read-back page corresponds to: unique element-count match, else `hint`. */
export function matchOpsPage(
  doc: OpsDoc,
  read: ReadPage,
  hint?: number,
): OpsPage | undefined {
  const byCount = doc.pages.filter((p) => p.elements.length === read.count);
  if (byCount.length === 1) {
    return byCount[0];
  }
  const hinted = doc.pages.find((p) => p.n === hint);
  if (hinted && hinted.elements.length === read.count) {
    return hinted;
  }
  return undefined;
}

/** Elements paired by index; a `line` whose read height exceeds leading*s*WRAP_FACTOR is flagged. */
export function flagWrapped(
  ops: OpsPage,
  read: ReadPage,
  s: number,
): WrapFlag[] {
  const flags: WrapFlag[] = [];
  ops.elements.forEach((el, i) => {
    const r = read.elements[i];
    if (!r || el.type !== "text" || el.kind !== "line") {
      return;
    }
    const expected = el.leading_pt * s;
    if (r.height > expected * WRAP_FACTOR) {
      flags.push({
        page_n: ops.n,
        index: i,
        text: el.text.slice(0, 40),
        expected_px: Math.round(expected * 100) / 100,
        read_px: r.height,
      });
    }
  });
  return flags;
}
