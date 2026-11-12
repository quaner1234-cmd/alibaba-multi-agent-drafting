# Alibaba B2B Multi-Agent Product Drafting Workflow

A **desensitized playbook and experiment log** for preparing industrial parts as
Alibaba.com B2B **drafts**: prepare once, execute serially, verify the actual save,
then hand the draft to a human reviewer. Roles are assigned per task, not per agent brand.

> Scope boundary baked into the process: **only save drafts, never submit/publish.**
> A human reviews and publishes. Every automation rule below serves that boundary.

## Why this exists

Publishing industrial parts on Alibaba.com is repetitive but full of UI traps:
lazy-loaded form sections, framework inputs that silently reject programmatic writes,
cross-origin asset banks, lookalike duplicate assets, and strict listing-compliance rules.
We turned one painful manual batch into a verified, repeatable multi-agent pipeline,
and this repo documents the method (not our store data).

## Latest recorded progress: 2026-11-12

- The executor now runs on a **native, persistent, human-logged-in Chromium** driven by
  a process-level SDK/CLI, replacing the earlier extension-scoped browser. A human signs
  in once; agent-opened pages inherit the session. See
  [setup-and-tools.md](docs/setup-and-tools.md).
- The run chain is a fixed **15-step pipeline** with category switching and product-group
  selection inserted before any field write. See
  [executor-pipeline.md](docs/executor-pipeline.md).
- **Pilot first, then batch** is now the rule: one real card end-to-end, record and fix
  every failure in the runner, re-run that card, then run the rest serially. Five separate
  observations in this window each ended with `SAVED_AND_READBACK_PASS` on every card;
  these are separate cohorts, not a cumulative store counter.
- A **600-card pool** across four packages was audited read-only. The official validator
  reported 600/600 `CARD_READY`; the auditor then found executor-side problems the
  validator does not check. After fixes the final classification was
  **BLOCKER 0 / BUSINESS 0 / QUALITY 4**. 255 cards previously held back were released
  once the runner gained category and group support.
- Business rules are now **versioned and single-sourced**, with a fingerprint in the
  state document so `--check` reports `STALE`. Older batches are not retroactively
  rewritten.
- Duplicate checking moved to the **preparer** (one check with handoff evidence); the
  executor no longer repeats it.
- 34 existing drafts were reviewed for a lead-time policy change: 27 corrected,
  7 already compliant, 0 failures, each verified by re-opening the same draft ID.

Read the [2026-11-12 observation](experiments/2026-11-12/README.md), its
[aggregate data](experiments/2026-11-12/aggregate.json), the
[measurement limits](docs/measurement-and-evidence.md) and the
[failure catalog](docs/pitfalls.md).

## Historical seed batch

- 10 products drafted end-to-end, **all re-opened from the server and read back field-by-field**
- 7 scored 5.0, 3 scored 4.9 ("excellent"); no submits, no duplicates, no compliance violations
- One pilot product was completed by a third agent to debug the pipeline; its verified
  steps were distilled into the workflow the other agents then consumed

These historical results describe the original cohort; they are not a fresh store
audit or a cumulative count across later batches. The 2026-11-08 entry is preserved
unchanged in the [experiment index](experiments/README.md).

## Roles: the human chooses who performs them

| Role | Scope |
| --- | --- |
| **Preparer** | Finalize fields/title and image order once; register image/video bank references; run **one** platform duplicate check and record the evidence in the handoff. May upload missing bank assets, but cannot edit products. |
| **Executor** | Consume the pinned card without repeating preparation. Real copy UI, category/group when required, fields/media, save and same-ID server readback. One writer, serial products; optional read-only dedup flag for review only. |
| **Tool maintainer** | Fix actual failures and improve repeated steps; not a mandatory second reviewer of each product. |
| **Human reviewer** | Review business/display details and decide whether to publish. |

Human checkpoints: approve the candidate list, approve publishing, resolve anything
outside agent authorization (logins, CAPTCHAs, permissions).

See [docs/roles-and-handoff.md](docs/roles-and-handoff.md).
For a bounded batch, use the
[pilot-then-batch prompt](templates/pilot-then-batch.prompt.md). The
[five-product-trial prompt](templates/five-product-trial.prompt.md) is the 2026-11-08
historical version.

## Repo map

```
docs/
  setup-and-tools.md      browser/runtime prerequisites, public tools, preflight checklist
  executor-pipeline.md    the current 15-step serial run chain and acceptance gates
  roles-and-handoff.md    role division, handoff contract, stop conditions
  workflow-six-stages.md  the conceptual stage machine and exit criteria
  publishing-rules.md     listing rules: banned words, title, codes, MOQ/weight, media
  browser-recipes.md      current native-browser recipes + historical extension recipes
  pitfalls.md             every trap we hit and the honest fix
  measurement-and-evidence.md  timing definitions and evidence limits
  tooling-status.md       local tool changes and what is not shipped here
experiments/
  README.md               chronological progress index
  2026-11-08/             historical report, anonymous JSON/CSV and phase observations
  2026-11-12/             aggregate-only observation brief and structured counts
scripts/
  export_experiment.py    allowlisted export from private result records
tests/
  test_export_experiment.py  public-export privacy and timing regressions
templates/
  workcard.example.json   the versioned workcard schema (placeholders)
  pilot-then-batch.prompt.md   current role-neutral execution prompt
  five-product-trial.prompt.md historical execution prompt
```

## Desensitization

Store identity, contacts, prices, listing IDs, asset IDs, draft IDs, session IDs,
credentials and absolute local paths are removed or replaced with placeholders
(`<MODEL>`, `<workspace>/`, `null`). Public tool names and links are kept because the
method depends on them: the current browser is
[ego lite](https://github.com/citrolabs/ego-lite) (a public, MIT-licensed Chromium
automation browser); the historical BrowserSkill / `bsk` recipes are kept as history
only. Internal policy numbers (MOQ, weight tiers) are kept in generic form — they are
the store's own publishing policy, not customer data. Operational browser scripts,
workcards, manifests, media and raw evidence remain private; this is not a turnkey
posting bot.

## Update and verify

Append a new observation directory when results arrive; preserve prior snapshots and
counterevidence. Use a private manifest outside this repository with
`scripts/export_experiment.py` when per-product rows are actually being exported; for
aggregate-only updates, publish counts with `null` for unrecorded timings and say so
explicitly. The exporter publishes only anonymous status/score, counts and timing
fields, never a raw result file. See [measurement guidance](docs/measurement-and-evidence.md).

Run `python -m unittest discover -s tests -v` before committing. The public suite
covers the exporter only. The separately reported operational test suite belongs to the
private workspace and does not prove live platform compatibility. Scan the staged diff
for private identifiers before pushing.

## License

MIT - see [LICENSE](LICENSE).
