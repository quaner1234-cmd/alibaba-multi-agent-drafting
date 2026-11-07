# Roles, handoff contract, stop conditions

## Division of labor

### Prep agent (offline, codename ZCode)

- **May**: web search for reference listings; platform queries in read-only tabs
  (dedup keyword search, template/category/unit inspection, image/video bank search);
  upload *missing assets to the asset bank* when that helps; generate derived images
  (e.g. a "Model: X" caption strip) with originals preserved; write versioned workcards.
- **Must not**: create/edit/save product drafts, submit, or touch drafts another agent
  or the human is editing.
- Delivers: `packages/<model>/<version>/workcard.json` + generated preview + snapshot hash.

### Executor agent (browser, codename Hermes)

- Consumes **only** workcards that passed the offline checks (`LOCAL_READY`, `TITLE_FINAL`).
- Runs the six stages serially: dedup, copy and fields, media, company content, save,
  fresh-server-page verification. One product fully verified before the next.
- Writes per-product result files with stage, status, evidence, timings, errors.

### Pilot/debugger agent (codename Codex)

- Used when the pipeline is new or broken: completes **exactly one** product with deep
  debugging (network captures, DOM/state inspection), then writes a HANDOFF + WORKFLOW
  document with verified steps and honest "unverified" boundaries.
- The executor explicitly skips the pilot product and consumes the distillation.
- This pilot-then-handoff pattern saved the second batch from re-losing hours to the
  same traps (title state commit, lazy-loaded sections, template entry point).

## Handoff contract

- Every handoff names: model, draft ID (or null), last verified stage, what is proven
  (server readback evidence) vs merely done (DOM/click ok), blockers, and browser state
  (sessions/tabs to reuse or clean).
- Status vocabulary - never inflate:
  - `LOCAL_READY` - offline checks passed; says nothing about the platform.
  - `TITLE_FINAL` - this exact title text (sha256-bound) passed semantic/compliance review.
  - `SAVED_UNVERIFIED` - real save success response captured; not yet read back.
  - `DONE/verified` - same draft ID re-opened fresh from the server and every required
    field/asset matched.
  - `SKIPPED` - platform already has this model (with search evidence).
  - `SAVE_UNKNOWN` - save result unobserved (e.g. extension disconnected); verify later,
    never blind-retry.
- Agent-to-agent notes live in a shared memory store; **work files live in the repo
  directories** so any agent can pick up cold.

## Concurrency and user-takeover rules

- If a re-open shows server values this round's agent could not have written, treat it
  as concurrent editing: **stop writing immediately**, keep evidence, report. Never
  overwrite with a stale snapshot.
- If the human takes over the browser tab ("user has control"), stop driving it.
- Cleanup is self-only: close your own tabs, stop your own session. Never kill the
  shared browser, daemon, or another agent's windows.
- Approvals: host permission gates are part of the system. A refused action is recorded
  and worked around *only* if a legitimate, authorized alternative exists - never bypassed.
