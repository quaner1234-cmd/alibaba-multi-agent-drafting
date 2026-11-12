# The current executor pipeline (2026-11-12)

The [six-stage machine](workflow-six-stages.md) is the conceptual contract. This page
describes the actual ordered step chain that implements it after the switch to a native
logged-in browser. All names are generic; no operational script, ID or path is shipped
here.

## One card, one serial run

Each product is one versioned workcard, consumed by one serial runner invocation. The
runner executes a fixed, ordered step chain and writes a per-product result record:

| # | Step | Purpose / constraint |
| --- | --- | --- |
| 1 | `copy` | Open a genuinely new draft through the real "publish similar" entry. Force a reload when the tab already points at the target URL, otherwise the previous product's gallery is still displayed. |
| 2 | `switch_category` | For non-default product families only. Must happen **before any field write**: the platform discards unsaved edits on a category change. |
| 3 | `set_product_group` | Pick the group from the store's existing tree. Free text is not accepted. |
| 4 | `preflight` | Company module/template, enum fields, guard checks; includes a slow server-side template load that cannot be optimised away. |
| 5 | `title` | Write the pinned title. |
| 6 | `price_tiers` | Add the second price-ladder row explicitly; the field writer validates row counts. |
| 7 | `remove_weight` | Delete the inherited custom "Weight" attribute row — it is not the logistics gross weight. |
| 8 | `fields` | Codes, condition, MOQ, lead-time quantity/days, gross weight, prices. |
| 9 | `main_images` | Ordered gallery; one batched upload is the only lossless speedup found. |
| 10 | `detail_images` | Upload one by one, checking the count after each. A multi-file drop produced duplicates or losses. |
| 11 | `customization` | Remove the default customised-packaging block (match by literal prefix, not a regex). |
| 12 | `selling_points` | The generator button is off-viewport; scroll it into view and allow a long bounded wait (short polling caused failures). |
| 13 | `videos` | Cross-origin iframe: use isolated-world evaluation to set the VID and dispatch input/change, then click inside the frame. Coordinate clicks fail. |
| 14 | `save` | Draft-only. Capture the business success response and the new draft ID. |
| 15 | `readback` | Re-open that same ID from the server and compare an ordered field list. `SAVED_AND_READBACK_PASS` is the only terminal success label used here. |

Steps 2 and 3 are no-ops for the default product family, so previously verified cards
are unaffected by the addition. Steps 11–12 are conditional on the card schema
generation. A dry run performs everything except save/readback and is reported as such;
it is never counted as a saved draft.

## Category switching

The real flow is: "switch category and sales mode" button → confirmation dialog
(warns that unsaved edits are lost) → a category-selection page → target entry matched
on normalized text → "I have read the rules, publish now" → back to the editor with the
new category ID. After the switch, inherited attributes, condition, price table, gross
weight, lead-time and company module all still need to be checked. The guarded field
writer requires the URL to still carry the "new template copy" flag, which the category
navigation drops. Restore that flag with `history.replaceState` — the page really is a
new template copy, so this restores true semantics rather than bypassing a guard.

A substring guard is not a category check: one family name is a substring of another,
and a naive `includes()` test silently accepted the wrong category. Switch explicitly
and read back the resulting category.

## Product groups

The group control is a tree of groups that already exist in the store. There is no
free-text input and no "create group" entry in the dropdown. Map the card's group label
to an existing store group explicitly; if no mapping exists, fail instead of silently
inheriting the default group. Click the tree node's **label** element — clicking the
surrounding `<li>` appears to work but leaves the value unchanged. Add the resulting
category and group to server readback.

## Pilot first, then batch

1. Validate the whole queue (`CARD_READY` for every card) and sync the state block.
2. Run **one** card for real. Record each new failure, fix the root cause in the runner,
   then re-run that same card. Do not "fix" a card by quietly editing a business value.
3. Only then run the rest serially. A single transient media failure is handled by
   re-running the whole card (up to a small retry bound), not by changing the asset or
   the card.
4. If several consecutive cards fail, stop the batch and preserve exact state.

## Resumability and state

- A draft registry plus the batch log form the skip set. Use their **union**; reading
  only one source silently re-queued an already-created product once.
- Read both as UTF-8 with BOM tolerance (`utf-8-sig`). A BOM written by a Windows shell
  made the first JSON line unparseable.
- Pass the registry path explicitly. Auto-detection by walking ancestor directories for
  a manifest fails for nested card packages and silently loses registrations.
- Resolve manifest card paths relative to the manifest's own directory, or use absolute
  paths; a child process with a different working directory otherwise exits immediately.
  Record the child return code and a stderr tail instead of an empty status.
- Business numbers live in exactly one rules file. The state document contains a
  machine-generated block with that file's fingerprint; `--check` reports `STALE` when
  the rules change, so a copied number in a second document cannot quietly go out of
  date.

## Dedup ownership

The preparer runs one duplicate check (drafts and published/all, including normalized
spellings) before a package is prepared, and writes the evidence into the handoff. The
executor does not repeat it; an optional read-only flag exists for manual review. Batch
skipping from the local registry is a resumability decision, not a platform duplicate
check. The trade-off is explicit: if the preparer omits the check, nothing downstream
intercepts a duplicate.

## Acceptance

`SAVED_AND_READBACK_PASS` requires a real save response, the new draft ID, and a fresh
server-page comparison covering category, group, MOQ, lead-time quantity/days, gross
weight, both price rows, condition, media counts/order and video associations. A
validator pass, a dry run, an `upload ok`, a click result or a process exit code are
never acceptance. Publication remains a separate human action.
