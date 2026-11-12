# Tooling status at the 2026-11-12 snapshot

This repository distributes a workflow, a public result exporter and prompt templates.
The operational helpers below exist in a separate private workspace; they are
documented here, not provided as a turnkey browser package. The 2026-11-08 snapshot is
preserved in the repository's history.

| Area | Change | Evidence | Remaining limit |
| --- | --- | --- | --- |
| Browser route | Moved from extension-scoped task spaces to a native, persistent, human-logged-in Chromium driven by a process-level SDK/CLI | Repeated logins disappeared; a read-only probe reports `LOGGED_IN` | A human still owns login, CAPTCHA and permissions; one account, one serial writer |
| Executor | Fixed 15-step serial chain, including category switch and product-group selection before field writes | One multi-family card ran for real with 11/11 server read-back fields passing; 255 held-back cards released | Sales unit is not written; 43 cards in one family differ from the copy source and remain platform-unverified |
| Card validator | Recomputes tiered weight, two price rows, title length/hash, image hashes, banned words, category/group guards | 600/600 `CARD_READY` across four packages | Generational validators are not interchangeable; an older one reported 11 false failures on newer cards |
| Whole-pool auditor | Read-only classification BLOCKER / BUSINESS / QUALITY / INFO, in addition to the validator | Found 97 category mismatches, 255 missing group writes and 439 padded titles while the validator was 100% green | A validator pass is not an executability guarantee |
| State sync | Machine block derived from the draft registry and manifests, with a fingerprint of the rules file | `--check` reports `STALE` when the rules file changes | Detects drift only for the fields it fingerprints |
| Batch runner | Resumable skip set = batch log ∪ draft registry; BOM-tolerant reads; explicit registry path; absolute manifest card paths; child exit codes and stderr tails | Re-runs no longer silently re-queue already-created products | Local skip logic is resumability, not a platform duplicate check |
| Readback verifier | Same saved ID re-opened from the server; ordered checks now include category, group, lead-time quantity/days and both price rows | All cohorts in the 2026-11-12 observation ended in `SAVED_AND_READBACK_PASS` | A save without readback stays `SAVED_UNVERIFIED` |
| In-place repair helpers | Targeted correction of lead-time days/quantity on existing drafts, with same-ID re-open | 27 of 34 drafts corrected, 7 already compliant, 0 failures | Repairs are counted separately from newly created drafts |
| Media handling | Six main images batched in one invocation; four detail images uploaded one-by-one with per-image count checks; isolated-world evaluation for the cross-origin video iframe | Measured main-image phase ~19 s → ~11 s in one layout | Transient `N not accepted` retries still occur; handled by whole-card re-run |
| Selling points | Scroll the generator into view and allow a long bounded wait | Short polling (300–350 ms) caused failures | Generator occasionally falls back to a generic value; those cards are flagged for human review |
| Automatic dispatch | Not implemented | The human chooses an agent and forwards the bounded task | n/a |

The private operational suite was reported at **239 passing offline checks** at this
snapshot. The public repository has its own exporter suite; these are different suites
and should not be presented as a single benchmark. Neither proves live upload
throughput, and a local test pass is never written up as a platform run that passed.

All items above are **local-only tool improvements**. No operational browser helper,
workcard, manifest, image, video or result registry is shipped in this repository.
