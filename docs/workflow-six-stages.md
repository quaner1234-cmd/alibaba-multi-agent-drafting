# The six-stage machine (per product)

| Stage | What happens | Exit criterion / record |
| --- | --- | --- |
| 1. Scope and dedup | Read latest state files; search platform "all/published" and "drafts" for the model **and its normalized spelling** (the platform strips `-`, `&`, `/`...) | No duplicate, proceed. Duplicate, `SKIPPED` with search evidence. Never modify existing listings. |
| 2. Copy and fields | Open a new copy through the real "Publish Similar Product" menu. Confirm draft-only listing type, category and source identity. Write product-specific codes, confirmed condition, prices/tiers and calculated logistics. Keep correctly inherited fixed values. | Component/derived values match the pinned card. A changed source is bound in a separate execution card; category changes require affected fields to be checked. |
| 3. Media | Consume the prepared order: 5 main images + 4 details, first detail's model cue already prepared. Select the registered non-FST video in both slots. | Light execution checks: counts, first image/basic order, obvious mixed products and actual dual-video association. No repeated source-authenticity, OCR, playback or byte audit. |
| 4. Company content | Preserve correctly inherited company content. If missing, apply the already-approved company module once inside the product. | Company content and approved card are present. Do not reapply a correct module or update the shared template. |
| 5. Detect and save | Run the platform quality check, fix *real* findings; trigger **Save** only | Capture the real business success response (e.g. `submitDraft` success URL with the draft ID). Record `SAVED_UNVERIFIED`. |
| 6. Server-page verification | Read the same saved ID on the server page reached after save; otherwise open a controlled new page. Refresh server data and compare fields/associations with ordered light receipts. | Required execution checks pass, `DONE/verified` with the actual score. A 4.9 with no substantive missing item is not repeatedly reworked for 5.0. Human review remains separate. |

## Ordering rules that saved the batch

- **Dedup is stage 1 for a reason**: the "publish similar" flow inherits the template's
  codes; missing a duplicate creates near-identical listings that are painful to unwind.
- **Ordered media**: a prepared batch can be selected/uploaded within one script call.
  Check actual resulting order; bank-list order is not product order. Preserve correct
  prefixes on resume rather than deleting/reuploading the whole gallery.
- **Save is stage 5, verification stage 6** - a save without stage 6 is `SAVED_UNVERIFIED`,
  and stage 6 needs the server's saved state, not the still-unsaved form. A same-ID
  post-save server page qualifies; another tab is not intrinsically required.
