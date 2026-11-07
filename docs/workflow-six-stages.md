# The six-stage machine (per product)

| Stage | What happens | Exit criterion / record |
| --- | --- | --- |
| 1. Scope and dedup | Read latest state files; search platform "all/published" and "drafts" for the model **and its normalized spelling** (the platform strips `-`, `&`, `/`...) | No duplicate, proceed. Duplicate, `SKIPPED` with search evidence. Never modify existing listings. |
| 2. Copy and fields | Open a **new copy via the listing's real "Publish Similar Product" menu** (never a hand-built copy URL - that silently edits the source product and creates overwrite-prone pseudo-drafts). Confirm listing type (business-opportunity product) and category. Fill title, model codes, condition `New`, group, price/MOQ, logistics quantity = MOQ, gross weight | Fields committed to components and derived summaries correct (e.g. a "4 pcs = $X" line refreshes). Category switch means re-check fields. |
| 3. Media | Exactly 5 main images + 4 detail images (first detail clearly shows the model), correct non-FST video linked in **both** main-video and detail-video slots | Counts, order, content verified in the gallery; both video slots matched by exact file name (cover-hash if lookalikes exist). |
| 4. Company content | Apply the platform company template (e.g. `Jennifer`) inside the current product only; replace the template's default business card with the store's approved card; keep other template content | Company gallery count intact, no foreign contact card left. **Never** save changes into the shared template. |
| 5. Detect and save | Run the platform quality check, fix *real* findings; trigger **Save** only | Capture the real business success response (e.g. `submitDraft` success URL with the draft ID). Record `SAVED_UNVERIFIED`. |
| 6. Fresh-server-page verification | Re-open the same draft ID from the server, trigger lazy loads, compare every field/asset in order | All required items match, `DONE/verified` with the score. A 4.9 "excellent" is recorded as 4.9, never rounded up. |

## Ordering rules that saved the batch

- **Dedup is stage 1 for a reason**: the "publish similar" flow inherits the template's
  codes; missing a duplicate creates near-identical listings that are painful to unwind.
- **First image first**: upload or insert the first main image and see it appear before
  uploading the rest, so concurrent completion cannot reorder the gallery.
- **Save is stage 5, verification stage 6** - a save without stage 6 is `SAVED_UNVERIFIED`,
  and stage 6 needs a *new* page load, not the still-open form.
