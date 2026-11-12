# The six-stage machine (per product)

The conceptual contract. The current executor implements it as a fixed 15-step chain —
see [executor-pipeline.md](executor-pipeline.md). Stage numbers here are the human-facing
checkpoints, not the runner's step count.

| Stage | What happens | Exit criterion / record |
| --- | --- | --- |
| 1. Scope and dedup | Read the latest state document and the current business-rules file; confirm the preparer's single platform duplicate check (published/all **and** drafts, including normalized spellings) is recorded in the handoff. | `CARD_READY` for the card, state check clean, dedup evidence present. Duplicate or stale rules: `SKIPPED`/`STOPPED` with evidence. Never modify existing listings. |
| 2. Copy and structure | Open a genuinely new draft through the real "Publish Similar Product" menu. **Before any field write**, switch category for non-default families and select the product group from the store's existing tree. Then write codes, confirmed condition, two price-ladder rows, MOQ, lead-time quantity/days and tiered gross weight. Keep correctly inherited fixed values. | Component/derived values match the pinned card; category and group verified on the server page after save. A changed source is bound in a separate card version. |
| 3. Media | Consume the prepared order: **6 main images + 4 detail images**. For one family the first detail image is a real gloved-hand model shot. Select the registered non-FST video in both slots. | Light execution checks: counts, first image/basic order, obvious mixed products and actual dual-video association. No repeated source-authenticity, OCR, playback or byte audit. |
| 4. Company content | Preserve correctly inherited company content. If missing, apply the approved company module once inside the product. The template's default contact card must not survive. | Company content and approved card are present. Do not reapply a correct module or update the shared template. |
| 5. Detect and save | Run the platform quality check, fix *real* findings; trigger **Save** only. | Capture the real business success response (e.g. `submitDraft` success URL with the draft ID). Record `SAVED_UNVERIFIED`. |
| 6. Server-page verification | Re-open the same saved ID from the server, trigger lazy loads, and compare an ordered field list: category, group, MOQ, lead-time quantity/days, gross weight, both price rows, condition, media counts/order, video associations. | `SAVED_AND_READBACK_PASS` with a real save response and a fresh server page. A save without stage 6 stays `SAVED_UNVERIFIED`. Human review/publication remain separate. |

## Ordering rules that saved the batch

- **Dedup is stage 1, owned by the preparer.** The "publish similar" flow inherits the
  template's codes; missing a duplicate creates near-identical listings that are painful
  to unwind. One check with evidence is enough — but if the preparer omits it, nothing
  downstream intercepts a duplicate.
- **Structure before fields.** A category switch discards unsaved edits, so it must
  happen right after the copy and before any field write. Groups are picked from a
  pre-existing tree, not typed freely.
- **Ordered media.** Main images can be uploaded in one batched invocation; detail images
  are uploaded one by one with a count check after each. Check the actual resulting
  order; bank-list order is not product order. Preserve correct prefixes on resume
  rather than deleting/reuploading the whole gallery.
- **Save is stage 5, verification stage 6** — a save without stage 6 is
  `SAVED_UNVERIFIED`, and stage 6 needs the server's saved state, not the still-unsaved
  form. A same-ID post-save server page qualifies; another tab is not intrinsically
  required.
- **Pilot one card first.** The first real card spends its time discovering layout
  failures; fix those in the runner and re-run that card before launching the rest of
  the batch.
