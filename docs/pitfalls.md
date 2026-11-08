# Pitfalls catalog (all encountered in production)

1. **DOM text is not component state.** Title/model/SKU/weight all showed new values
   after execCommand or paste, yet the first save submitted old data. Fix: native
   setter + events + a real Tab per field + server readback.
2. **A hand-built `pubAction=copy` URL is not "copy".** It opens the *source product's*
   edit page; saving creates a same-ID pseudo-draft that overwrites other pseudo-drafts
   of that product. Only the list menu's "Publish Similar Product" creates a genuinely
   new draft (new item ID after save).
3. **The pilot cost is real but pays back.** The first product took the longest; the
   distilled handoff let the next nine run on verified steps instead of rediscovery.
4. **Canvas smart-inputs** refuse fill/selector writes; click to materialize, target
   the real input, verify on reload.
5. **Asset banks have different surfaces**: some observed picker iframes were
   cross-origin; a later uploader iframe was same-origin and exposed real inputs.
   For lookalike video rows, register name/VID/non-FST together. "Linked count"
   counters did not move on draft association; never use them as acceptance.
6. **`upload ok` / `click ok` / exit 0 are delivery receipts, not outcomes.** Acceptance
   is always: business response plus fresh-server-page readback.
7. **Virtual lists and cached badges** fake both "no results" and "still there".
   Control queries and list re-opens are part of the evidence.
8. **Toggle submenus** ("Edit v") close on the second blind click. Fresh observation
   between clicks.
9. **Idle reaping** destroys unsaved forms. No mid-form waits; batch decisions up front.
10. **Minimized window** produces geometry errors that look like UI races. Restore first.
11. **Promo dialogs** re-appear after every save or reload and cover the whole a11y
    tree; their close buttons are icon-only (find by class).
12. **Policy changed mid-project** (gross weight became unit x MOQ + 3 kg). Old verified
    drafts were not retroactively "wrong-proofed": rule updates do not rewrite history;
    each old record stays evidence of its own era's rules.
13. **Short-code rejections**: the platform rejected a too-short OE code; the full
    source-model spelling (with its parenthetical) normalized correctly - do not invent
    padding digits.
14. **Category switch wipes attributes**: after changing category, re-fill the cleared
    attribute fields (found during stage-6 verification).
15. **Template default card**: the company template ships with someone else's contact
    card - find it in the company gallery (hover reveals the delete control) and replace
    it with the store card in-product only.
    Once the approved module contains the correct card, preserve it on later copies
    rather than repeating the replacement.
16. **Verified playback was not verified registration.** Text splitting paired video
    names with adjacent rows' IDs. The selected VID was sometimes FST despite an earlier
    "content confirmed" label. Extract name/VID/non-FST from one row and verify the
    saved association; do not repeat the whole preparation audit downstream.
17. **Built-in CUA can still be global.** One preparation agent's window-level controls
    coincided with an extension HUD/frame-access failure in the executor's tab. A
    clean rebuilt copy saved successfully. This is an observed association, not proof
    of the extension's universal root cause; isolate actual input scope.
18. **Wall times overlap.** One delayed product span included executing three other
    products before returning to rebuild it. Summing those four spans double-counts
    time. Keep overlap tags and report the shared batch window separately.
19. **Scripts were already in use.** Scalar fields were about a minute; multi-minute
    media phases contained many observations and response gaps. Optimization should
    combine repeated UI steps, not merely add another reviewer or another upload tool.
20. **Bank IDs can contradict existing metadata.** If one ID is assigned to different
    recorded file hashes, route those slots to selected local files. Do not silently
    equate them or begin a full image-authenticity project.
21. **A company module is not a complete product template.** Company content already
    reused a module; clean-source copying of all fixed fields still needed a real
    trial. Keep candidate plans, successful UI copying and inherited-field evidence
    as separate states. Always replace product-specific media, prices and codes.
