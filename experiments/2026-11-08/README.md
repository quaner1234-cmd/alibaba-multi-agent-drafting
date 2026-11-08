# 2026-11-08: preparation handoff and media execution

## Scope and outcome

This is a follow-up cohort, separate from the historical seed batch in the root
README. Ten private executor result records say `DONE`, `verified=true`, with zero
recorded missing items: nine injectors scored 4.9 and one pump scored 5.0. The drafts
were saved as inquiry/business-opportunity products, not submitted. Final human
review/publication is not established by these records.

The source records were read for this export; products were not re-audited on the
platform and source photos were not reviewed again.

Data: [results.json](results.json), [results.csv](results.csv),
[interaction/preparation observations](observations.json).
Earlier index revisions, three-sample preparation and seven pump records are in
[preparation history](preparation-history.md); its unfinished 3.9 result is preserved.

## Recorded timing

| Anonymous product | Wall-clock span | Caveat |
| --- | ---: | --- |
| P01-P04 | Unknown | Named field/save commands exist; no complete wall timing |
| P05 | 52m02s | Recovery/correction included; two save-command durations on the same draft |
| P06 | 36m52s | Recorded product span |
| P07 | 3h58m09s | Delayed/rebuilt; includes execution of P08-P10 in the middle |
| P08 | 48m35s | Recorded span; retries and tab recovery included |
| P09 | 32m03s | Recorded span; 56 tool calls; model/provider changes confound comparisons |
| P10 | 28m05s | Recorded span; inherited unrelated scene images had to be removed |

For P07-P10 the enclosing interval is **3h58m09s**, not the sum of their overlapping
spans (**5h46m52s**). It includes recovery, pauses and other work and is not a normal
single-product estimate. The raw anonymous rows retain relative start offsets so
the overlap remains inspectable.

The P09 native event log gives a more useful breakdown:

| Phase | Window from first dispatch through last completion | Nested command duration |
| --- | ---: | ---: |
| Five main images from bank | 238s | Batch selection command: 40s |
| Four detail images | 124s | Local uploads command: 39s |
| Main + detail video association | 260s | Existing bank entries selected; no video upload |

These phase windows include observations/response gaps and use explicit event
boundaries; they are not transfer-only timing or phases to add to the nested commands.
They exclude unrelated later pauses. Different phase boundaries can produce slightly
different rough conversational estimates.

**Inference:** reducing separate model/UI decisions is a promising next change. The
data does not show that bank selection is always faster, that the network upload is
the only bottleneck, or that one model is faster than another.

## Preparation and discovered errors

- Two five-product preparation handoffs registered 45 image slots and five non-FST
  videos each. The first reported 15 new upload slots/30 reused slots; the resumed
  handoff reported 9/36. Complete active-work timing is unknown. These are slot counts,
  not globally unique asset counts or completed product drafts.
- Name/VID extraction by splitting page text had paired non-FST names with neighboring
  FST IDs. Same-row DOM extraction corrected the association. An earlier playback
  check did not prove that the stored name/VID pair was correct.
- One stuck form had a foreign extension HUD/frame-access denial while another agent
  was using CUA. After deferral and authorized rebuilding, a clean copy saved. This
  sequence does not establish a universal extension root cause.
- Separate readback-tab creation also failed behind stuck tabs. Capturing fresh
  server data on the same-ID page reached after save completed the readbacks.
- The next five cards contain obvious bank-registration conflicts: one bank ID mapped
  to different already-recorded file hashes. The new routing uses selected local
  files for 2/2/2/6/4 positions respectively, without a new source-photo audit.

## Changes prepared, not yet proven faster

1. Combine fresh UI observations and media actions within a bounded helper call;
   select registered videos rather than re-uploading or re-playing them.
2. Reuse an approved company module and correctly inherited fixed fields. Try a clean
   same-category copy source on the first normal product, with a known-source fallback.
3. Read the saved server page directly and use ordered light UI receipts for known
   filename transformations. Preserve strict behavior for explicit diagnostic use.
4. Assign preparer/executor/tool-maintainer roles to whichever agent the human chooses;
   avoid downstream re-preparation and unnecessary per-product stop/confirmation loops.

The private operational suite passed 210 offline tests. Five execution cards and an
agent-neutral prompt were prepared. No completed result records for that trial were
observed at this snapshot; an in-flight form cannot be excluded merely from missing
results. **Live compatibility, inherited-copy behavior and speedup remain unverified.**

## Next observation

Record actual five-product results, real copy inheritance, media helper success vs
narrow fallback, wall time and automatically collected stage timings. Keep quality
scores accurate; do not rework a complete 4.9 simply to reach 5.0. New results should
be appended as another observation, not substituted for this pre-trial snapshot.
