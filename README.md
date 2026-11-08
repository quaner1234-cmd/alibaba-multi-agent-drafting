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

## Latest recorded progress: 2026-11-08

- A follow-up cohort has **10 executor-recorded saved/read-back drafts**, no recorded
  missing items: nine scored 4.9 and one scored 5.0. Human approval/publication is separate.
- A 32m03s example used 56 tool calls. Selecting five main images took 40s inside one
  command; uploading four detail images took 39s inside one command. Full UI phases
  were longer because they included observation and response gaps.
- Two preparation cohorts registered 45 image slots and five non-FST videos each.
  These are registration counts, not new physical assets or completed product drafts.
- A further five-product trial has prepared cards and local tool changes, with
  **runtime compatibility and speed still unverified**. No claimed speedup or model ranking.
- [Earlier preparation/pump history](experiments/2026-11-08/preparation-history.md)
  preserves candidate-pool revisions and seven pump records, including one 3.9
  saved-but-unverified result. These cohorts are not combined into a global count.

Read the [experiment report](experiments/2026-11-08/README.md),
[anonymous CSV](experiments/2026-11-08/results.csv), and
[measurement limits](docs/measurement-and-evidence.md).

## Historical seed batch

- 10 products drafted end-to-end, **all re-opened from the server and read back field-by-field**
- 7 scored 5.0, 3 scored 4.9 ("excellent"); no submits, no duplicates, no compliance violations
- One pilot product was completed by a third agent to debug the pipeline; its verified
  steps were distilled into the workflow the other agents then consumed

These historical results describe the original cohort; they are not a fresh store
audit or a cumulative count across later batches.

## Roles: the human chooses who performs them

| Role | Scope |
| --- | --- |
| **Preparer** | Finalize fields/title and image order once; register image/video bank references. Supplied packages are trusted. May upload missing bank assets, but cannot edit products. |
| **Executor** | One platform duplicate check before creation, real copy UI, fields/media, save and same-ID server readback. Consume the handoff without repeating preparation. One writer, serial products. |
| **Tool maintainer** | Fix actual failures and improve repeated steps; not a mandatory second reviewer of each product. |
| **Human reviewer** | Review business/display details and decide whether to publish. |

Human checkpoints: approve the candidate list, approve publishing, resolve anything
outside agent authorization (logins, CAPTCHAs, permissions).

See [docs/roles-and-handoff.md](docs/roles-and-handoff.md).
For a bounded batch, use the [agent-neutral five-product prompt](templates/five-product-trial.prompt.md).

## Repo map

```
docs/
  roles-and-handoff.md    agent division of labor, handoff contract, stop conditions
  workflow-six-stages.md  the stage machine each product goes through, with exit criteria
  publishing-rules.md     listing rules: banned words, title length, code consistency,
                          MOQ & gross-weight policy, image counts, company template
  browser-recipes.md      tested browser-automation recipes (the hard-won part)
  pitfalls.md             every trap we hit and the honest fix
  measurement-and-evidence.md  timing definitions and evidence limits
  tooling-status.md       local tool changes and what is not shipped here
experiments/
  README.md               chronological progress index
  2026-11-08/             report, anonymous JSON/CSV and phase observations
scripts/
  export_experiment.py    allowlisted export from private result records
tests/
  test_export_experiment.py  public-export privacy and timing regressions
templates/
  workcard.example.json   the versioned workcard schema (placeholders)
  five-product-trial.prompt.md  transferable execution prompt with placeholders
```

## Desensitization

Store identity, contacts, prices, listing IDs, asset IDs and internal paths are removed
or replaced with placeholders (`<MODEL>`, `<workspace>/`, `null`). Agent codenames and
the browser-automation tooling (BrowserSkill / `bsk`, a public project) are kept because
the method depends on them. Internal policy numbers (MOQ/weight) are kept in generic
form - they are the store's own publishing policy, not customer data. Operational
browser scripts and raw evidence remain private; this is not a turnkey posting bot.

## Update and verify

Append a new observation directory when results arrive; preserve prior snapshots and
counterevidence. Use a private manifest outside this repository with
`scripts/export_experiment.py`. The exporter publishes only anonymous status/score,
counts and timing fields, never a raw result file. See [measurement guidance](docs/measurement-and-evidence.md).

Run `python -m unittest discover -s tests -v` before committing an exporter change.
The public suite covers the exporter. The separately reported operational test suite
belongs to the private workspace and does not prove live platform compatibility.

## License

MIT - see [LICENSE](LICENSE).
