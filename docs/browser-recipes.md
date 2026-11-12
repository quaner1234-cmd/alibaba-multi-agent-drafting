# Browser automation recipes

These are observations from specific layouts, not guarantees for every current page.
Two routes are recorded: the **current** native logged-in Chromium route (2026-11-12)
below, and the **historical** extension/CLI route (2026-11-08) later in this file.
Recipes from one route are not automatically valid for the other.

## Native logged-in Chromium (current, 2026-11-12)

The executor drives a desktop Chromium with a persistent, human-logged-in profile via a
process-level SDK/CLI. See [setup-and-tools.md](setup-and-tools.md) and
[executor-pipeline.md](executor-pipeline.md).

- Each CLI invocation starts a short-lived process (~2 s of overhead). Real speed comes
  from **batching repeated steps into one invocation**, not from adding more single-step
  calls.
- Locators must resolve to exactly one element that is inside the viewport. Scroll the
  target into view first; tag the first match when the DOM has duplicates. Keyboard and
  mouse input can only be added incrementally to an existing script, not replaced
  wholesale.
- Framework-controlled inputs: click → select → `Input.insertText` → native setter, then
  re-read the value. A single merged setter that returns `undefined` is not a write.
- Lazy-loaded dropdowns (company template): one short probe can return zero options
  (`no template option`). Poll in bounded rounds (e.g. 2 × 8 s) and allow one re-open of
  the dropdown.
- A suggestion overlay left open by a previous field can intercept pointer events on the
  next field. Close floating layers (bounded Escape rounds) before writing, then use the
  native setter plus a page-level Enter. The symptom is a timeout on a selector that
  *did* match exactly one input.
- Cross-origin video iframe: walk the frame tree, create an isolated world for that
  frame, set the VID in that world with `input`/`change` events, then click inside the
  frame. Coordinate clicks and top-page evaluation do not reach it.
- Detail images: upload one at a time and verify the count after each, against a
  relative baseline. A `N not accepted` failure was one-off jitter — re-run the whole
  card (up to a small retry bound), never change the asset or the card.
- Main images: one batched upload of all positions is both faster and lossless
  (~19 s → ~11 s in one layout). Cross-group duplicate images are allowed; only check
  for duplicates within a group. Recognize both `1.jpg` and `xxx(1).jpg` source names.
- After a category switch the editor reloads and the URL loses the "new template copy"
  flag; restore the true flag with `history.replaceState` before the guarded field
  writer runs. Perform the category switch **before** any field write — unsaved edits
  are discarded.
- Product groups are a pre-existing tree: no free-text input and no create entry. Click
  the node's **label** element; clicking the surrounding `<li>` leaves the value
  unchanged (`group not applied` on a dry run).
- The selling-points generator button sits outside the viewport and needs a long
  bounded wait; short polling (300–350 ms) caused failures.
- Registries: read with BOM tolerance (`utf-8-sig`). A UTF-8 BOM written by a Windows
  shell made the first line unparseable and silently re-queued already-created products.
- Save and verify: capture the business save response with the new draft ID, then
  re-open that same ID from the server. Promo dialogs re-appear after every reload.

## Historical extension/CLI route (2026-11-08, retired for this workflow)

Assumes the BrowserSkill extension+CLI model:
`cooperate sync` returns a `context_id` (plus a fresh `observation_id`) that
DOM-targeted actions require; element refs (`@eN`) re-number on every observation.
The sections below are kept as history; new integrated helpers remained
runtime-unverified at that snapshot.

## Session discipline

- Start per task: `session start --browser <instance>`; close your own tabs
  (`tab close`) and `session stop` when done - even on failure.
- Idle sessions are reaped (~5 min) **together with unsaved forms**. Never pause
  mid-form; save stage progress only when allowed and safe, or run the form
  start-to-finish.
- A minimized agent window reports viewport 0x0 and every geometry-dependent call
  fails with misleading errors ("pointer target moved", "could not resolve geometry").
  Restore the window first.
- After a wedge ("A page frame is not responding"), inspect the original operation,
  native dialog and ownership first. Preserve unsaved work; do not reload or stop a
  session just to recover control. Do not blind-replay the last action.

## Reading pages

- `cooperate sync` then `observe` (a11y tree) is the workhorse. Follow
  `@more observe --cursor ...` immediately; cursors expire fast and a fresh sync
  invalidates them.
- Cross-origin iframes (asset banks) are invisible to `evaluate` but usually reachable
  via a11y refs - and vice versa. Probe both before declaring something unreadable.
- Virtualized tables render only visible rows: scroll and sample, or use the list's own
  search, to enumerate. Page-count badges can cache; re-open the list to trust them.

## Writing fields (the single most valuable recipe)

Framework-controlled inputs silently accept DOM writes while committing nothing:

- `el.value = ...` and `execCommand('insertText')` / paste can update the DOM and the
  character counter, yet the **component state keeps the old value** - the first save
  then submits stale data.
- Reliable sequence per field: native setter + `input` + `change` events, **then a real
  Tab keystroke on that same field** (via a11y ref), then re-observe to confirm the
  value survived a re-render; final acceptance only on the re-opened server page.
- Canvas-backed "smart inputs" may not materialize their real `<input>` until clicked;
  `fill`/selector writes bounce off. Click the row first, re-observe, target the
  materialized input.
- Tag-style selects (OE codes): free-typing works - `fill` the input, take the **new
  ref from fill's own output**, send `Enter` on that ref. The platform strips symbols
  (`AB-12` becomes `AB12`); that is normalization, not failure. Delete tags via the
  tag's inner close icon (`.next-tag-close-btn`), not the tag body. Never save an empty
  required tag field; equal-value duplicate tags may all vanish when you close one.
- Numbers: verify the *derived* line ("4 pcs = $40"), not the input box.

## Images

- Main-image slots: clicking the slot usually opens the asset-bank picker
  (cross-origin). The local-upload path is a hover menu ("Local upload") whose button
  only exists in the a11y tree after hover - ref each time, never reuse.
- Some templates expose a hidden multi-file `input[type=file]` per gallery: reveal it
  (store the original style, force visible/positioned), take a fresh ref, upload with
  the ref and multiple `--file` args, verify thumbnails, then restore the original
  style. React re-renders rebuild the input between uploads - re-reveal every time.
- A later asset-bank uploader had a same-origin iframe with a real file input/drop
  area. That route successfully preloaded missing images. Earlier picker limitations
  do not establish that every bank route is blocked.
- Use existing prepared registrations without a second content audit. Registered bank
  selection and direct local upload are both valid paths; measure their complete UI
  phases rather than claiming one is universally faster.
- In a measured example, four local detail uploads completed inside one 39s command.
  The surrounding UI phase was longer. Put repeated, freshly observed actions in one
  bounded helper invocation to avoid a model decision between every small action.

## Video

- The asset-bank upload page has a real `input[type=file]` hidden at 0x0 - reveal it,
  take a fresh ref, upload with `--mode input`, then wait for the name plus thumbnail
  and the business completion response. An `upload ok` alone proves nothing.
- "Already exists" is a *duplicate guard*, not an error: go reuse the existing asset.
- Bank registration uses name search and same-row extraction of name/VID/non-FST status.
  On the product selector, the observed VID field can target that prepared registration.
  Match the name in that same result row; splitting all page text on "VID:" previously
  paired a non-FST name with the adjacent FST row's ID.
- Product side: the main-video dialog ("select from video bank") and the detail-video
  dialog ("select detail video") have identical buttons - read the dialog title.

## Save and verify

- Verify the real Save control and use an authorized observed pointer/keyboard path.
  Unknown native dialogs must be identified first; an overlay is not permission to
  blindly press Space or bypass a tool refusal.
- `click ok` does not mean persisted. Capture the business save response
  (`submitDraft` returning a success URL that contains the new draft ID), then open
  that ID fresh, trigger lazy loads (scroll, detail-editor init), and compare
  everything in order.
- If Save already navigated the task tab to the same ID's server page, read fresh
  server render data there. A separate reader tab is optional. This avoided repeated
  new-tab failures caused by another stuck task tab in the observed run.
- The light path uses ordered UI receipts (actual names/asset URLs) to resolve known
  suffix stripping/server renaming. It does not download/hash every image; unresolved
  order stays unresolved and gets a narrow quick check.
- The structured-detail editor is lazy: its iframe/toolbar do not exist until you
  scroll to the section (and possibly tick a mode radio). Reading it before init
  returns a false zero.
- After any save the page reloads and re-shows promo dialogs - close them and re-read.
