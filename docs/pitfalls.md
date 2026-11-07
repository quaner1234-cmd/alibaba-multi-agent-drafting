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
5. **Asset banks**: picker iframes are cross-origin (unreachable from evaluate);
   uploader pages expose real inputs (reachable). Lookalike assets (FST suffix, same
   name) are picked by exact name plus cover hash, and "linked count" counters do not
   move on linking - never use them as acceptance.
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
