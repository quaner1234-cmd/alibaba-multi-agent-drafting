# Setup and tools (2026-11-12)

This repository is a method record, not a runnable posting bot. The operational browser
helpers, workcards, manifests, media assets and result registries stay in a private
workspace. This page lists what must be in place before the workflow can be run, naming
public tools only where they are genuinely public.

## 1. A logged-in Chromium browser an agent can drive

- Use a desktop Chromium automation browser that shares **one persistent,
  human-logged-in profile** across newly opened pages. We use
  [ego (lite)](https://lite.ego.app/) and its `ego-browser` JavaScript SDK / CLI
  ([MIT source](https://github.com/citrolabs/ego-lite),
  [quick start](https://lite.ego.app/document/en/docs/quick-start)). A human signs in to
  the store once; agent-opened pages inherit that session.
- **Why the extension route was retired.** Some extension-based agents give each task
  space its own isolated browser context. A store login that lives in one tab then
  disappears when that tab or space closes, causing repeated QR logins. The earlier
  BrowserSkill / `bsk` recipes in [browser-recipes.md](browser-recipes.md) describe that
  retired route and are kept as history, not as the current setup.
- Give the agent a **dedicated task space** (`<task-space>`) with its own name. If a
  human already owns a space with that name, choose another; never claim, close or reset
  a human-owned space or session. The persistent profile is shared, so the new space
  still sees the login.
- **One account, one executor.** Product creation is serial. A second concurrent writer
  on the same account can produce colliding drafts.
- Human-only actions: initial login, CAPTCHA, permissions, any account-level change,
  and the final publication decision.

## 2. Local runtime

- Python 3.x. This public repository needs only the standard library; the private
  workspace may add its own packages. On Windows, force UTF-8 output
  (`python -X utf8 ...`) so registries and logs stay parseable.
- A private workspace rooted at `<workspace>/` containing:
  - one versioned workcard (JSON) per product, a batch manifest with **absolute** card
    paths, and a `created.jsonl` registry of saved drafts;
  - prepared media (ordered main/detail images, non-FST video registrations) and their
    hashes;
  - a per-product result directory and a batch log.
- No credentials, cookies, session IDs, task-space IDs, account names, product codes,
  prices, draft IDs, media IDs or raw assets are ever placed in this public repository.

## 3. Five small local tools that make the method work

| Tool | Responsibility |
| --- | --- |
| Card validator | Read-only gate. Recompute policy-derived fields (weight tier, price-ladder rows, title length/hash, image hashes, banned words, category/group guards). A card is `CARD_READY` or `CARD_INVALID`. Generational validators are **not** interchangeable: an older version reports false failures on newer cards. |
| State sync | Recompute the machine-readable state block from the draft registry and manifests. `--check` fails when the state block or the **business-rules file fingerprint** is stale. Business numbers live in exactly one file. |
| Batch runner | Serial queue with resumability: skip set = batch log union draft registry, both read with BOM tolerance. Stop after consecutive failures; record child-process exit codes and stderr tails. |
| Readback verifier | Re-open the same saved draft from the server and compare an ordered field list; emit `SAVED_AND_READBACK_PASS`. |
| Card auditor | Read-only whole-pool audit classifying findings as BLOCKER / BUSINESS / QUALITY / INFO. It runs **in addition to** the validator, because a validator can be 100% green while the executor still fails on a field the validator never checks. |

All five live in the private workspace. This repository documents their contract, not
their code. Keep tool changes labelled as local-only improvements; an offline test pass
does not establish current-page compatibility.

## 4. Preflight checklist

1. Human has approved the candidate list, the business-rules version and the
   draft-only boundary.
2. Browser installed, logged in, and a fresh read-only probe reports `LOGGED_IN`.
3. State sync `--check` is clean; the rules-file fingerprint matches.
4. Validator reports `CARD_READY` for every card in the queue.
5. Preparer has delivered **one** duplicate check with evidence; the executor does not
   repeat it.
6. One pilot card is run for real; its failures are fixed before the rest of the batch.
7. Save is draft-only. Publication remains a separate human action.

See [executor-pipeline.md](executor-pipeline.md) for the run chain and
[publishing-rules.md](publishing-rules.md) for the rule shapes.
