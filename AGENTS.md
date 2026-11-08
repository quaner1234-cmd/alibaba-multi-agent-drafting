# Repository instructions

This is a public, desensitized workflow and experiment record. Operational store
files, browser sessions and execution scripts live outside this repository.
Read README.md and the current experiment entry before changing claims.

- Roles are assigned by the human for each batch; do not require a named agent.
- Keep draft creation, actual save, server readback and final human approval distinct.
- Append subsequent experiment observations under experiments/. Preserve earlier
  snapshots and failures; unknown timing is null, not zero. Never sum overlapping
  product spans or rank models from mixed-model runs.
- Publish measured timings, counts, methods, changes and unresolved limits. Remove
  store identity, contacts, account information, actual product codes, prices,
  product/media IDs, browser/session IDs, credentials and absolute local paths.
- Use scripts/export_experiment.py with a private manifest outside this repository
  for result exports. Never stage the private manifest, raw conversations, browser
  snapshots or product assets. Scan the final staged diff before pushing.
- Document local-only tool improvements as such. This repo does not contain the
  operational browser helpers; tests here validate the public exporter only.
- On receiving new authorized experiment results, update the experiment index,
  data snapshot and relevant conclusions, then test, commit and push to the existing
  branch. This instruction does not start agents, schedule polling or publish products.

Validation: `python -m unittest discover -s tests -v`.
