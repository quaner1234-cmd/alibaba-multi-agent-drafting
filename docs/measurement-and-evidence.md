# Measurement and evidence boundaries

## What a timing number means

- **Product span:** recorded start to finish, including observations, waiting and
  recovery. It may contain another product's work. Tag overlap instead of summing it.
- **Command duration:** a named tool/script's actual run time. Field scripts and a
  save can add up to about a minute while the product span is tens of minutes.
- **UI phase window:** first tool dispatch through the final tool completion for a
  defined phase. It includes intermediate observations and model/dispatch gaps, not
  just network transfer. The example's four-detail upload command is part of its
  detail phase, not an additional independent duration.
- **Batch elapsed time:** the enclosing batch interval with overlap counted once.
  Do not add product spans that overlap. Do not treat a first generated artifact's
  timestamp as the true start of preparation or as active-operation time.
- **Unknown:** JSON null / empty CSV cell. Never substitute script time or zero.

If a model/provider changes during execution, keep the same target and preserve the
switch as a confounder. Different products, recovery incidents and light/strict
inspection levels are also confounders. This dataset does not support model rankings
or a causal speedup percentage.

## Evidence scope

The published rows are derived from private executor result records. They preserve
the recorded status, verified flag, score and missing-item count. This export is not
a new live store audit. Original receipts/conversations/media are not public.

Local checks, bank registration, UI association, business save, same-ID server
readback and human approval are distinct claims. A source-workspace test pass does
not establish current-page compatibility. Planned changes remain unverified until
the assigned real product trial produces results.

## Updating the public log

1. Keep the private result files and private product-to-P01-style mapping outside
   this repository. Each manifest product supplies `public_id`, generic `kind`,
   `result_path`, and optionally `timing_scope=overlapping_recovery_span`.
2. Use a new observation directory:

   ```text
   python scripts/export_experiment.py --manifest <private-manifest> --out experiments/<date-or-run>
   ```

   The exporter is create-only and uses an explicit field allowlist. It does not
   copy notes, model codes, IDs, prices, source paths or arbitrary nested fields.
3. Add a concise report: measured outcome, changed method, known failures, timing
   definition and what remains unverified. Link the experiment in the index.
4. Reconcile totals against JSON/CSV, validate relative links and scan the staged
   diff for source identifiers, credentials and commercial data.
5. Commit/push the authorized update and verify the remote branch SHA. Keep older
   observations intact. Receiving data does not start another execution agent or a
   background monitoring service.

The public exporter tests use synthetic fixtures. Operational source helpers and
their separate tests are not distributed in this repository.
