# Roles, handoff contract and stop conditions

## Assign roles per task

The human chooses a preparer, an executor and, when needed, a tool maintainer.
Historical agent codenames are provenance, not exclusive responsibilities.

- **Preparer:** prepare fields, final title, selected image order and asset-bank
  references once. Run **one** platform duplicate check (published/all and drafts,
  including normalized spellings) and put the evidence in the handoff. Trust the
  supplied package. Upload missing bank assets when authorized; preserve original
  files. Do not create, edit, save or submit products.
- **Executor:** consume the pinned card and registrations. Do not re-search titles,
  authenticate source photos, replay videos, audit the old bank **or repeat the
  duplicate check**. Confirm this step's target, actual writes, ordered associations,
  save and same-ID server readback. An optional read-only dedup flag exists for manual
  review, not for routine runs.
- **Tool maintainer:** handle real tool/layout failures and reusable improvements;
  not a routine second product reviewer. A normal completed draft goes to the human.
- **Human:** resolve material business facts and review the finished draft for publication.

**Why dedup moved:** two agents each running one check wasted time and still left the
same blind spot. One check with written evidence is cheaper and equally safe — but the
trade-off is explicit: if the preparer omits it, nothing downstream intercepts a
duplicate. Batch skipping from a local `created.jsonl` registry is *resumability*, not a
platform duplicate check; never conflate the two.

## Handoff contract

Give each product a versioned card with a source locator and hash. Include final
fields, explicit condition/tier decisions, the active `rules_version`, ordered local
paths, registered bank names/IDs, the exact non-FST video registration, the dedup
evidence and a **short** list of remaining blockers only. Raw cards, draft IDs and
platform IDs remain private, outside this public repository.

- Pin the exact execution card before browser work. Bind a changed copy source in a
  separate card version only after observing the real copy entry/URL. Preserve old cards.
- The manifest carries an `exec_ready` flag per card. Cards that need a capability the
  executor does not yet have are held back, with the reason recorded — not silently
  skipped. Release them only after a real pilot proves the capability.
- Manifest display fields (for example a group label shown in a queue review) must be
  kept in sync with the card contents; a stale display field makes the queue misleading.
- For a partial product, keep its real target ID, last completed stage, uncertain
  operation, missing items and task-owned browser state. Continue that target.
- A missing result file is not evidence that nobody has started the product.
- Prepared bank assets do not imply product association, save or business readiness.
- Revisit only a missing/changed item, obvious contradiction or platform rejection.
  Do not send the whole product through preparation again.
- Business numbers live in one rules file. The executor's state document carries that
  file's fingerprint and `--check` reports `STALE` on a mismatch; a card that disagrees
  with the rules goes back to the preparer.

## Status vocabulary

| Label | Meaning |
| --- | --- |
| `CARD_READY` / `CARD_INVALID` | Read-only validator outcome for a card. Not a save. |
| `DRY_RUN_MEDIA_OK` | All steps performed except save/readback. Never counted as a draft. |
| `SAVED_UNVERIFIED` | Real business save response captured, but no server readback yet. |
| `SAVED_READBACK_FAIL` | Save happened, but the same-ID server comparison disagreed. |
| `SAVED_AND_READBACK_PASS` | Real save response, new draft ID, and a fresh server page whose ordered fields all match. |
| `SAVE_UNKNOWN` | Reconcile the original request/server before repeating any save. |
| `SKIPPED` / `STOPPED` | Already-existing product, or a batch halted after consecutive failures. |

A tool refusal, an unknown write effect, a validator pass, a dry run, an `upload ok`,
a click result or a process exit code is **not** acceptance. None of these mean human
approval or publication.

## Batch and browser ownership

- Use one writer for a queue and serial product creation. Run **one pilot card for real**
  first, fix each new failure in the runner, re-run that card, then continue the rest of
  the assigned batch; do not stop after every product.
- Stop the batch after several consecutive cards with no draft, preserving exact state
  and child-process exit codes/stderr tails.
- The current browser is a native, persistent, human-logged-in Chromium with a
  process-level SDK/CLI. Give the agent its **own named task space**; never claim,
  close or reset a human-owned space. The persistent profile is shared, so a new space
  still sees the login. Window/desktop CUA can compete for global mouse/keyboard focus;
  preparers yield desktop input to the executor.
- Isolate a product-specific failure and continue safe independent work. Stop early
  for a global account/tool blocker, preserving the exact state.
- An unexplained server change or human takeover stops writes to that target. Never
  restore a stale snapshot over another editor.
- Clean only task-owned tabs/sessions. Do not kill shared browsers, restart shared
  daemons, dismiss unknown native dialogs or switch tools to bypass a refusal.
