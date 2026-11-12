# Pilot-then-batch prompt template (2026-11-12)

A role-neutral, copyable prompt for a human to hand to an executor. Replace every
`<placeholder>` locally. Keep the private business-rules file outside this repository.
The `five-product-trial.prompt.md` template in this directory is the 2026-11-08
historical version and is preserved as-is.

---

> We are creating **drafts only** on the store. Never submit and never publish.
>
> **Before you start**
> 1. Read the current state document and the current business-rules file. Business
>    numbers come only from the rules file; do not copy them into any other document.
>    If the state check reports `STALE`, stop and ask.
> 2. Confirm the browser is installed, the human has logged in, and a read-only probe
>    reports `LOGGED_IN`. Use a dedicated `<task-space>`; never claim a human-owned one.
>    One account, one serial writer.
> 3. Confirm the preparer has delivered **one** duplicate check with evidence. You do
>    not repeat it.
> 4. Confirm every card in `<queue>` is `CARD_READY` under the current rules version.
>
> **Pilot**
> 5. Run exactly one card for real, end to end: copy → (switch category / set group if
>    required) → preflight → title → price ladder → remove inherited attribute row →
>    fields → ordered main images → detail images one by one with a count check →
>    customization → selling points → videos → save → server read-back.
> 6. Write down every failure, its root cause and the exact fix. Fix the **runner**, not
>    the card: do not quietly change a business value to make a step pass. Re-run the
>    same pilot card until `SAVED_AND_READBACK_PASS`.
> 7. Report the pilot result before continuing. If I do not confirm, stop.
>
> **Batch**
> 8. Run the remaining cards serially. Skip set = batch log ∪ draft registry; read both
>    with BOM tolerance. Pass the registry path explicitly.
> 9. A single transient media failure: re-run that whole card up to `<retry-bound>`
>    times. Do not change the asset or the card. If several consecutive cards fail,
>    stop and preserve exact state.
> 10. Each card must end in `SAVED_AND_READBACK_PASS` with a real save response, a new
>     draft ID, and a fresh server-page comparison of category, group, MOQ, lead-time
>     quantity/days, gross weight, both price rows, condition, media counts/order and
>     video associations. A validator pass, dry run, `upload ok`, click result or exit
>     code is not acceptance.
>
> **Report back**
> - A table: count, saved-and-read-back passes, failures, retries, median and range of
>   per-card seconds, and any `null` timing written as "not recorded".
> - The list of new failures and what you changed in the runner.
> - A short list of remaining blockers only; do not list every skipped product.
> - State explicitly: "drafts only, no submission, no publication; human approval is
>   still required."
>
> **Never include in any public artifact**: product codes, prices, draft IDs, media IDs,
> account or contact details, session IDs, credentials, raw conversations, browser
> snapshots, product assets or absolute local paths.
