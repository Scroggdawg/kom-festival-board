# handoff-083-connectors

## Where we left off

**This turn (Sep 16, 2026, Fable 5.1, a duck, no build):** Luke pasted the
claude.ai connector directory's Design category and asked for three or four
useful connectors per project (Petrol, Pantheon, Adaptive Canvas, OpenClaw),
then three or four more that are not on that list. The shortlist is below.
Nothing was toggled, installed, or wired.

- **Sep 8** — handoff-082-festival: SCAD Savannah ruled not Oscar-qualifying; two ledger discrepancies logged, still unfixed.
- **Sep 7** — handoff-081-festival: the Joan call's writing notes isolated to a one-page PDF.
- **Sep 6** — Claude-surfaces raid filed: playbook plus two ducks, awaiting Luke.

**Direction we were going:** this repo is the festival lane. This turn is a
cross-project tooling question parked here because it is where Luke asked it;
the lane tag `connectors` is new and stays a one-off unless the question recurs.

---

- **timestamp:** 2026-09-16 11:25 PDT (from `date`)
- **lane:** connectors
- **continues:** handoff-082-festival.md (different lane; seam cross-reference, no earlier connectors handoff exists)
- **model:** Claude Fable 5.1 (`claude-fable-5-1`), desktop Code tab
- **turn:** ducks. A recommendation, not a build. Fable ran a duck turn here, which is off the default (Opus for ducks).

## How the picks were made

- Projects read from doctrine (`BETTER_DRIVER.md` per-project next moves, `BIG_VISION.md` adaptive surface, `SETUP.md` machine roster) and the folders on disk: `~/Petrol Coffee/petrol-brand-bible` (Blender set files under `blender/`, lanes for welder, press, compressors, tire changer), `~/Code/pantheon` + `~/Code/pantheon-native` (Expo SDK 54 iOS app, Supabase, Vercel, Whisper, Withings), `~/Adaptive Canvas` (empty, seed stage), `~/.openclaw` (OpenClaw 2026.5.19: agents, bluebubbles, canvas, flows, delivery-queue, media, memory).
- Already connected in this session: Figma, Canva, Adobe for creativity, Vercel, Supabase, Google Drive, Google Calendar, Gmail, AllTrails.
- Off-list candidates were checked against the MCP registry search, so "directory" versus "local MCP" is verified, not guessed. Home Assistant and Blender have no directory connector. GitHub did not surface in registry search; it is a first-party integration.
- Status pill colours use the widget's CSS role tokens. The dataviz validator was run first and FAILs by design on status colours (categorical-only scope); filed as a memory so the next session does not repeat the round trip.

## The shortlist (IDs are the part labels; say "P3 no, P4 yes")

### Petrol (site build, Blender set, brand)

| ID | Pick | Status | Use |
|---|---|---|---|
| P1 | Figma | connected | Site design to code; shaders and motion context for the web-side VFX; tokens mirror BRAND.md |
| P2 | Adobe for creativity | connected | Logos via vectorize and background removal; HSL, tint and colour overlay on renders; font search and type palettes; PDF and print |
| P3 | Trimble SketchUp | add (Design list) | Only 3D-modelling connector on the list. Block shop-shell and bay geometry, export DAE/OBJ into Blender. A round-trip, not Blender-native: trial it |
| P4 | SVGator | add (Design list) | Animated SVG mark and hero motion; the VFX that ships on the web |
| P5 | Blender MCP (ahujasid/blender-mcp) | local MCP, not in directory | Direct scene control from Claude Code, Poly Haven assets, Hyper3D. The real Blender-side answer |
| P6 | Shopify (official) | directory, other category | Products, orders, customers, shop info; matches BETTER_DRIVER's Shopify item |
| P7 | ComfyUI MCP server | local MCP, not in directory | GPU look-dev before CPU renders; same logic as the MacroCarbon contact-sheet rule |
| P8 | Klaviyo | directory, other category | Funnel email off store data; pairs with the funnel-raid-records work |

Bench: Rams (design review of agent-written UI), Octopus.do (sitemap), Streamline Icons, Print.com (labels and stickers priced from chat), Jockey (render-library search), Brandfetch (equipment-brand references for set dressing). Skipped on purpose: every website builder on the list (B12, Onepage, Sitelas, Lanlan, WebsitePublisher, Macaly) competes with the Shopify + Vercel stack.

### Pantheon (nutrition and fitness app)

| ID | Pick | Status | Use |
|---|---|---|---|
| PA1 | Figma | connected | Screens and components for React Native; Figma variables can mirror the 123-knob token manifest |
| PA2 | Mobbin | add (Design list) | Real food-logging and macro-dashboard flows as reference |
| PA3 | Rams | add (Design list) | Design review of the screens agents write; fits the pixel-gate discipline |
| PA4 | Epicure | add (Design list) | Flavour-pairing intelligence for the meal-plan generation route |
| PA5 | Expo (official) | directory, other category | Builds, build logs, EAS, App Store reviews; BETTER_DRIVER's EAS item as a connector |
| PA6 | Sentry | directory, other category | Crash and error triage across native and the API routes |
| PA7 | Maestro MCP | local MCP, not in directory | Plain-English regression suite ("log a meal, check the macro total"); BETTER_DRIVER item 3 |

Three off-list picks, not four: XcodeBuildMCP (BETTER_DRIVER item 1) is superseded by the desktop app's built-in iOS Simulator tool, present in this session. PostHog only earns a slot if Pantheon gets a second user. Bench: Stark, Streamline Icons, Appllama, ElevenLabs (Whisper already covers speech-to-text), Mermaid Chart for architecture docs.

### Adaptive Canvas (home gateway, the adaptive surface)

| ID | Pick | Status | Use |
|---|---|---|---|
| AC1 | tldraw | add (Design list) | A canvas Claude draws on; closest thing on the list to a surface composed per instant |
| AC2 | Figma | connected | Design the surface's states; shaders for ambient visuals |
| AC3 | ElevenLabs | add (Design list) | Voice in and out for the house. Adds the untrusted-input leg of the trifecta; review before wiring |
| AC4 | Mermaid Chart | add (Design list) | Gateway diagrams as validated SVG: tools that act versus the read-only feed, the allowlist |
| AC5 | Home Assistant MCP server | local, self-hosted integration | The reference gateway shape from doctrine; no directory connector exists |
| AC6 | AccuWeather | directory, other category | This-instant weather; ships its own Claude widgets |
| AC7 | Spotify | directory, other category | Now-playing as ambient state; the jam-session lineage |
| AC8 | n8n | directory, other category | Self-hosted triggers on the Hive, tailnet-only; chosen over Zapier because the gateway never gets a public endpoint |

Bench: Yodeck (push the surface to a wall screen), HyperFrames (motion panels), Streamline Icons.

### OpenClaw (the Hive's agent harness)

| ID | Pick | Status | Use |
|---|---|---|---|
| OC1 | Devil's Advocate | add (Design list) | Structured adversarial pass before a decision. Same family as the agent, so it does not satisfy the mixed-jury law; call-codex still does |
| OC2 | Fabric | add (Design list) | Personal knowledge base search (files, notes, bookmarks, recordings) as a memory backend |
| OC3 | Jockey by TwelveLabs | add (Design list) | Index the shop lanes' photo and video plates so an agent can find "the photo of peg R3" |
| OC4 | Mermaid Chart | add (Design list) | Flow diagrams for `flows/` and handoffs, syntax-checked and rendered |
| OC5 | n8n | directory, other category | Workflow runner the agents can call; webhooks and schedules on the Hive |
| OC6 | Firecrawl | directory, other category | Web, paper and GitHub search for the research raids |
| OC7 | Slack (official) | directory, other category | A fleet channel with threads and canvases; only if Slack is in use anywhere |
| OC8 | Inkbox | directory, other category | Hosted iMessage, SMS and email for agents. Routes messages through a third party; BlueBubbles works today, so only if the bridge keeps breaking |

Skipped on purpose: monday.com (competes with notes.json as the truth), Twilio (its connector is docs-only, two tools, not a sender), Sharable Link and Send (outward publishing; needs Luke's OK per item).

## Two things OpenClaw needs to know

1. OpenClaw cannot toggle claude.ai connectors. It attaches the same remote MCP URLs in `openclaw.json` with its own OAuth. The registry gave endpoint URLs for every directory pick (for example `https://mcp.notion.com/mcp`, `https://mcp.expo.dev/mcp`, which answers 401 until authorised).
2. Since April 2026 Claude usage routed through OpenClaw bills outside the subscription (doctrine, verified). Every connector added there is metered spend.

## Next step (one action for Luke)

Reply with yes or no per ID, for example "P4 yes, P3 no, AC5 yes". The yeses get toggled on (directory) or installed (local MCP) in a goose turn, one at a time, with a per-item OK before anything outward-facing.

## Open questions

- Is Slack in use anywhere? OC7 only matters if yes.
- Does Pantheon ever get a second user? Decides whether analytics earns a slot.
- Which ComfyUI MCP server: several community builds exist; pick one in the goose turn after checking maintenance dates.

## FILES

- This handoff: `/Users/scroggdawg/Code/kom-festival-board/handoffs/handoff-083-connectors.md`
- Previous handoff (festival lane): file:///Users/scroggdawg/Code/kom-festival-board/handoffs/handoff-082-festival.md
- Per-project next moves in doctrine: file:///Users/scroggdawg/BMF%20Headquarters/DOCTRINE/BETTER_DRIVER.md
- Petrol Blender set README: file:///Users/scroggdawg/Petrol%20Coffee/petrol-brand-bible/blender/README.md
- Memory filed this turn: file:///Users/scroggdawg/.claude/projects/-Users-scroggdawg-Code-kom-festival-board/memory/dataviz-validator-status-colours.md
- Blender MCP: https://github.com/ahujasid/blender-mcp
- Home Assistant MCP server integration: https://www.home-assistant.io/integrations/mcp_server/
- Maestro MCP: https://docs.maestro.dev/getting-started/maestro-mcp
- XcodeBuildMCP (superseded here): https://github.com/cameroncooke/XcodeBuildMCP
- One ComfyUI MCP server candidate: https://github.com/joenorton/comfyui-mcp-server

file:///Users/scroggdawg/Code/kom-festival-board/handoffs/handoff-083-connectors.md
