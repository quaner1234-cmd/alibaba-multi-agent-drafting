# Alibaba B2B Multi-Agent Product Drafting Workflow

A **desensitized playbook** for publishing diesel fuel-injection parts to Alibaba.com
(B2B international) as **drafts** - research, offline preparation, browser drafting,
server-side verification - run by a small team of AI agents with human checkpoints.

> Scope boundary baked into the process: **only save drafts, never submit/publish.**
> A human reviews and publishes. Every automation rule below serves that boundary.

## Why this exists

Publishing industrial parts on Alibaba.com is repetitive but full of UI traps:
lazy-loaded form sections, framework inputs that silently reject programmatic writes,
cross-origin asset banks, lookalike duplicate assets, and strict listing-compliance rules.
We turned one painful manual batch into a verified, repeatable multi-agent pipeline,
and this repo documents the method (not our store data).

## Results from the batch this was distilled from

- 10 products drafted end-to-end, **all re-opened from the server and read back field-by-field**
- 7 scored 5.0, 3 scored 4.9 ("excellent"); no submits, no duplicates, no compliance violations
- One pilot product was completed by a third agent to debug the pipeline; its verified
  steps were distilled into the workflow the other agents then consumed

## The three roles

| Role | Local codename | Scope |
| --- | --- | --- |
| **Prep agent** (offline) | ZCode | Search references, finalize titles, verify facts/images/video, dedup research, write versioned workcards. **No browser writes.** |
| **Executor agent** (browser) | Hermes | Platform dedup check, open "publish similar" copies, fill fields, upload media, save draft, re-open and verify on a fresh server page. **Serial, one product at a time.** |
| **Pilot / debugger** | Codex | Completes exactly one product end-to-end with deep debugging, then writes a verified step-by-step handoff so the executor stops rediscovering traps. |

Human checkpoints: approve the candidate list, approve publishing, resolve anything
outside agent authorization (logins, CAPTCHAs, permissions).

See [docs/roles-and-handoff.md](docs/roles-and-handoff.md).

## Repo map

```
docs/
  roles-and-handoff.md    agent division of labor, handoff contract, stop conditions
  workflow-six-stages.md  the stage machine each product goes through, with exit criteria
  publishing-rules.md     listing rules: banned words, title length, code consistency,
                          MOQ & gross-weight policy, image counts, company template
  browser-recipes.md      tested browser-automation recipes (the hard-won part)
  pitfalls.md             every trap we hit and the honest fix
templates/
  workcard.example.json   the versioned workcard schema (placeholders)
```

## Desensitization

Store identity, contacts, prices, listing IDs, asset IDs and internal paths are removed
or replaced with placeholders (`<MODEL>`, `<workspace>/`, `null`). Agent codenames and
the browser-automation tooling (BrowserSkill / `bsk`, a public project) are kept because
the method depends on them. Internal policy numbers (MOQ/weight) are kept in generic
form - they are the store's own publishing policy, not customer data.

## License

MIT - see [LICENSE](LICENSE).
