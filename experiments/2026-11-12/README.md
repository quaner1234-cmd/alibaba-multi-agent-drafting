# 2026-11-12 — native-browser executor, pilot-first batching, whole-pool audit

**Status of this entry:** a desensitized observation log. It records workflow changes,
aggregate counts, measured timings and unresolved limits. It is **not** a live store
counter, not a quality-score report, and not a per-product result export. No product
codes, prices, draft IDs, media IDs, account names or local paths appear here.

Earlier entries are preserved unchanged; see the [index](../README.md). Cohort aliases
are local to this entry. Timings from different cohorts are **not** summed: some runs
shared an overlapping recovery window, and the model/provider changed between sessions,
so no speed ranking or causal speedup percentage is claimed.

## What changed since 2026-11-08

- The executor moved from an extension-scoped browser to a **native, persistent,
  human-logged-in Chromium** driven by a process-level SDK/CLI. This removed repeated
  logins caused by per-task-space browser contexts; see
  [setup-and-tools.md](../../docs/setup-and-tools.md).
- The run chain became a fixed 15-step pipeline with category switching and product-group
  selection inserted before any field write; see
  [executor-pipeline.md](../../docs/executor-pipeline.md).
- Duplicate checking moved from the executor to the **preparer** (one check, with
  evidence in the handoff). The executor keeps an optional read-only flag for review.
- Business rules became versioned and single-sourced: a tiered gross-weight formula
  replaced a fixed add-on, lead-time days became a fixed policy value, and the state
  document now carries a fingerprint of the rules file so `--check` can report `STALE`.
  Older batches are not retroactively rewritten.
- Media preparation moved to six ordered main images plus four detail images, with the
  first detail image required to be a real gloved-hand model shot for one family.
- A read-only **whole-pool card auditor** was added alongside the per-card validator,
  because a 100% green validator had coexisted with executor-side failures.
- Resumability hardened: skip set = batch log ∪ draft registry, BOM-tolerant reads,
  explicit registry path, absolute manifest card paths, and child exit codes in the log.

## Measured cohorts (aggregate only)

| Cohort | Cards | Saved + read-back pass | Transient retries | Median / range per card (s) | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | 26 | 26 | 4 | 87.4 / 69–155 | One rules generation; pilot card failed on a lazy-loaded template dropdown, fixed, re-run; several transient detail-image retries. Pure execution 2365 s across a longer wall-clock window that included debugging — do not add to other cohorts. |
| C2 | 5 | 5 | 1 | null | First card 78.0 s; one transient media retry. No aggregate timing recorded. |
| C3 | 5 | 5 | 1 | 92.8 / null | New card pool; one transient detail-image retry. |
| C4 | 5 | 5 | 0 | 95.7 / null | Corrected-title cohort; zero retries and zero media jitter. |
| C5 | 1 | 1 | 0 | null | Capability proof for multi-family support: 11/11 server read-back fields passed. |

`null` means "not recorded", not zero. All five cohorts were draft-only: no submission
and no publication.

## Other measured work in this window

- **In-place repair, 34 existing drafts:** lead-time days were brought to the new policy
  value. 27 were corrected, 7 were already compliant, 0 failures; about 22 s each. A
  separate earlier repair fixed one draft whose inherited lead-time quantity did not
  match its MOQ. Repairs re-opened the same draft ID and verified the value.
- **Whole-pool audit, 600 cards across 4 packages:** 600/600 `CARD_READY` from the
  official validator. The auditor initially classified 97 category mismatches, 255
  missing group writes, 439 padded titles and 6 exact-threshold weight cases. After the
  fixes below, the final classification was **BLOCKER 0 / BUSINESS 0 / QUALITY 4**
  (four intentionally unchanged older titles); weight, price-ladder, lead-time, MOQ,
  image hash, banned-word and cross-package duplicate findings were all 0.
- **Executor capability change:** 255 cards previously held back because they required a
  category switch and a group write were released after the runner gained both steps.
  One of them was then run for real with full server read-back.
- A private offline suite was reported at 239 passing checks at this snapshot. It is a
  different suite from this repository's public exporter tests; neither proves live
  platform compatibility.

## Failures recovered, and the lesson each left

| Failure | Root cause | Fix |
| --- | --- | --- |
| `no template option` on first pilot | Company-template dropdown loads options asynchronously; a single short probe read zero options | Bounded polling with a limited re-open, not a longer fixed sleep |
| MOQ and lead-time quantity disagreed on a saved draft | A missing card field was written as the literal string `None` into a numeric input, so the template's inherited value survived | Derive quantity from MOQ in the adapter; add both quantity and days to server read-back |
| Saved drafts silently missing from the registry | Registry auto-detection walked ancestor directories for a manifest and skipped nested packages | Pass the registry path explicitly |
| Already-created products re-queued | Windows shell wrote a UTF-8 BOM; `json.loads` failed on the first line of the registry | Union of log + registry, read as `utf-8-sig` |
| Batch child processes exited in 0.2 s with empty status | Manifest card paths were relative and the child had a different working directory | Resolve against the manifest directory / use absolute paths; record return code and stderr tail |
| `Category differs from checked workcard` guard did not fire | One family name is a substring of another, so an `includes()` check passed wrongly | Explicit category switch plus server-side category read-back |
| Guarded field writer refused to write after category switch | Category navigation dropped the "new template copy" URL flag | Restore the true flag with `history.replaceState` |
| Group value unchanged after a "successful" click | The tree needs a click on the node **label**, not the surrounding `<li>` | Target the label element and verify the resulting value |
| `detail image N not accepted` | One-off upload jitter, not a bad asset | Re-run the whole card up to a small retry bound; never change the card or asset |
| Business number copied into a second document went stale | Two documents each held their own copy of a rule value | One rules file, machine block with its fingerprint, `--check` reports `STALE` |
| 439 titles padded with a repeated filler phrase to reach the length floor | Preparer optimised for a validator metric | Replace with substantive wording and recompute length/hash; add an auditor check beyond the validator |

## Unresolved limits (do not read as pass)

- 43 cards in one family carry a sales unit that differs from the copy source; the
  runner does not write sales unit. Unverified on the platform.
- The selling-points generator occasionally falls back to a generic value after two
  failed attempts; those cards are marked for human review.
- Group labels are mapped semantically onto groups that already exist in the store. A
  human has not yet confirmed every mapping; the mapping is a convention, not a verified
  store taxonomy.
- Four older saved drafts retain the padded titles because the repair instruction
  deliberately excluded already-published-to-draft work.
- No publication, human approval, quality score, or per-product result rows were
  exported in this update. There is no private result manifest in this repository.

## Files in this entry

- `README.md` — this brief.
- `aggregate.json` — the same aggregate counts in structured form, with `null` for
  unrecorded timings. No per-product rows.

## Verification performed for the repository itself

`python -m unittest discover -s tests -v` (public exporter suite only) and a scan of the
staged diff for private identifiers. See the [measurement guide](../../docs/measurement-and-evidence.md)
for what these checks do and do not prove.
