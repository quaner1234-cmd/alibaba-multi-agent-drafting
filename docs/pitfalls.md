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

### Added 2026-11-12 (native-browser executor)

22. **One source is not a skip set.** Reading only the batch log (or only the draft
    registry) silently re-queued an already-created product. Use the **union** of both.
23. **BOM breaks JSONL.** A Windows shell writing UTF-8 with a BOM made `json.loads`
    fail on line 1, so the registry looked empty. Read registries and logs as
    `utf-8-sig`.
24. **Auto-detected registry paths.** Inferring the registry by walking ancestor
    directories for a manifest fails for nested card packages and silently loses
    registrations. Pass the registry path explicitly.
25. **Relative manifest card paths + a different child cwd.** Batch children exited in
    0.2 s with `FileNotFoundError` and a log line containing only `status: null`.
    Resolve card paths against the manifest's own directory (or use absolute paths) and
    record `returncode`/`stderr_tail`.
26. **Lazy-loaded template dropdowns.** A single 350 ms probe returned `n: 0`
    (`no template option`). Fixed with bounded polling rounds and one permitted re-open
    — not a longer unconditional sleep.
27. **A missing optional field is not "empty".** A card without lead-time quantity caused
    the literal string `None` to be typed into a numeric input; the template's inherited
    value survived while MOQ was 4. Derive quantity from MOQ and add both quantity and
    days to server readback.
28. **Business numbers copied into two documents go stale.** A state document still
    said "+3 kg" while the rules file had already switched to a tiered allowance. One
    canonical rules file, a fingerprint in the state block, and `--check` reporting
    `STALE` fixed the root cause.
29. **`includes()` is not a category guard.** One family name is a substring of another,
    so the guard silently accepted the wrong category. Switch explicitly and read the
    category back from the server.
30. **Category navigation drops the "new template copy" flag.** The guarded field writer
    then refused to write. `history.replaceState` restores true semantics — the page
    really is a new template copy — rather than bypassing the guard.
31. **Clicking a tree `<li>` does nothing.** The group control needs a click on the
    node's **label**. The first dry run failed with `group not applied` while every
    click appeared to succeed.
32. **Generational validators are not interchangeable.** An older validator reported 11
    false failures on newer cards. Use the validator for that schema generation, with an
    explicit version match.
33. **`detail image N not accepted` was jitter, not a bad asset.** Re-run the whole card
    up to a small retry bound; never change the image or the card to "fix" it.
34. **Price ladders need their second row added explicitly.** Without it the field writer
    throws a row-count mismatch. The inherited custom "Weight" attribute row is a
    separate trap: it is not the logistics gross weight and must be deleted.
35. **A 100%-green validator is not executability.** A whole-pool audit of 600 cards
    found 97 category mismatches, 255 missing group writes and 439 padded titles while
    the official validator reported 600/600 `CARD_READY`. Add an auditor that checks
    fields the executor actually writes, not just card shape.
36. **Optimizing for a validator metric degrades the artifact.** Repeating a filler
    phrase to reach the 118-character title floor produced 439 low-quality titles;
    deleting the filler dropped them below the floor. Fix with substantive sourced
    wording and recompute length/hash together.
37. **Manifest display fields drift.** A `group` shown in a queue review was still the
    old default for every card while the cards themselves were correct. Keep display
    fields in sync so reviews are not misleading.
38. **An in-place repair is not a save.** Correcting an existing draft must re-open the
    same ID and read back the changed value; count repairs separately from newly
    created drafts.
