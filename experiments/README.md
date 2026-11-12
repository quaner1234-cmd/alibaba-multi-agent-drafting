# Experiment log

| Observation | Scope | Status |
| --- | --- | --- |
| [2026-11-08](2026-11-08/README.md) | Follow-up ten-product cohort, media preparation, recovery and next five-product protocol | Ten recorded drafts complete; new integration runtime-unverified |
| [2026-11-12](2026-11-12/README.md) | Native-browser executor, 15-step pipeline, pilot-first batching, versioned rules, 600-card pool audit and in-place draft repairs | Draft-only; aggregate counts and timings recorded; per-product rows not exported |

This is an observation log, not a live store counter. Product aliases are local to
each cohort. Preserve earlier data and append later trial observations; do not sum
cohorts or overlapping spans without establishing their relationship.

The 2026-11-12 entry is **aggregate-only**: no private result manifest was part of that
update, so no anonymous per-product JSON/CSV was produced. `null` means "not recorded",
not zero. A validator pass, a dry run, an offline test suite and a same-ID server
read-back are distinct evidence classes; see
[measurement-and-evidence.md](../docs/measurement-and-evidence.md).
