# Listing rules (store policy, generic form)

These encode the store's own compliance and logistics policy. The numbers are the
store's choices; the *shape* of the rules is the reusable part. The authoritative
version lives in one private rules file. This document describes the current shape;
exact values, batch exceptions and the active version id stay in that file.

## Banned words (title/keywords)

- Brand words, even in compatibility form ("for X"): Bosch, Denso, Delphi,
  CAT/Caterpillar, Cummins, Perkins, Toyota, Mitsubishi, Volvo, Isuzu, Komatsu, Kubota,
  Yanmar, John Deere, Stanadyne, Zexel, Siemens, VDO, Continental.
- Authenticity/absolute words: Genuine, Original, Official, Copy, Replica, Best, No.1,
  Top-rated.
- Product-word risk: do not name this product family "Solenoid valve" (logistics/customs
  sensitivity) - use the accepted category wording.

## Title

- Natural sentence, **118-126 chars (hard cap 128)**, model number complete.
- Every category/technical word must have a source (the part's real numbering series,
  the platform catalog, or the physical asset). Never pad with unsupported fitments,
  brands, or tech words.
- Store brand prefix allowed; never borrow competitor branding.
- **Do not pad to reach the length floor.** Repeating a filler phrase to satisfy a
  validator produced hundreds of low-quality titles. Add substantive, sourced wording
  instead, then recompute `title_length` and `title_sha256` together. Length/hash
  agreement is necessary, not sufficient: an auditor should also check that the wording
  is meaningful.

## Code consistency and actual engine codes

1. OE code - **the platform normalizes away `-`, `&`, `/`...**; compare using the
   normalized value (`AB-120030` = `AB120030`).
2. Engine code - preserve an actual sourced engine code when present; it may differ
   from the part model. Use a model fallback only under the batch's approved rule.
   Record N/A only when the field is genuinely not applicable.
3. Model (attributes) - exact source spelling.
4. Custom attribute "Product name" - pure model code, no decorations.

Plus: SKU/spec fields inherited from the template must be re-checked for the old model.
A substring test is **not** a category check: one family name is a substring of another,
so `includes()` can silently accept the wrong category. Switch explicitly and read back
the resulting category from the server.

## Rule versions and non-retroactivity

- Every card carries a `rules_version`. Different generations coexist: older batches
  keep the rule set they were verified under; new preparation uses the current one.
- Rule updates do **not** rewrite history. An in-place repair to an existing draft is a
  separate, explicitly authorized action, and must re-open the same draft ID and verify
  the changed value.
- Business numbers must exist in **exactly one** file. Copying a value into a second
  document let one copy go stale for half an hour. The state document carries a
  fingerprint of the rules file and `--check` reports `STALE` on a mismatch.
- When a card and the rules file disagree, the rules file wins; send the card back to
  the preparer rather than editing the value in the executor.

## MOQ and logistics

- MOQ by real product category: injectors 4, pumps 1, everything else 10 (category of
  the *product*, not of words in the title).
- Lead-time quantity **= MOQ**. Derive it from MOQ in the adapter rather than leaving it
  optional: a missing field was once written as the literal string `None` into a numeric
  input, so the template's inherited quantity survived while MOQ was 4.
- Lead-time days = the rules file's **uniform fixed value** for the batch, not the
  template's inherited value. Both quantity and days are verified on the saved server
  page.
- Gross weight (platform field) uses a **tiered packaging allowance**:

  ```text
  moq_total_kg = unit_weight_kg * MOQ
  extra_weight_kg = 1.5  if moq_total_kg < 3 kg
                    2.0  if moq_total_kg >= 3 kg   (exactly 3 kg belongs here)
  gross_weight_kg = moq_total_kg + extra_weight_kg
  ```

  This replaced an earlier fixed allowance. Record unit weight, MOQ total, allowance
  and computed gross weight separately; the validator recomputes the tier and rejects a
  mismatch. Never write the single-unit weight; never multiply without the allowance.
- The inherited custom attribute row named "Weight" is **not** the logistics gross
  weight. Remove that row; do not confuse it with the shipping field.
- Price ladder: **two rows** (base and the batch's tier). Add the second row explicitly —
  the field writer validates row counts and throws otherwise. Tier prices require their
  own approved batch basis; a copied tier structure does not authorize the inherited
  price or discount. Compute decimal currency exactly.
- Batch exceptions must bind rule version, batch, actual category and explicit product
  scope together; a weight exception never leaks to every pump.

## Images and video

- Main images: exactly **6**, in the pinned numeric order. Detail images: exactly **4**.
  For one family the first detail image is a **real gloved-hand model shot**
  (`01_glove_model.jpg`); a legible engraving is not required because a human reviews
  it. If no such photo exists, fall back to the model-note image and flag it for review.
  Four *different* views are required (same shot with a different logo or crop does not
  count).
- If the source set has no legible-model image, generate a caption variant ("Model: X"
  in the white margin) with the original preserved and the derivation recorded; never
  fake an engraving.
- Video: the preparer registers name, VID and non-FST status from the **same row**.
  The executor uses that registration directly, then confirms both actual associations
  on the saved server page. Do not repeat video playback at every handoff.
- Trust supplied/selected images. Upload/register once, then check counts, first image,
  basic order and obvious mixed products. Full byte downloads/OCR/authenticity checks
  are exception diagnostics, not the standard workload. A caption is a model note,
  not evidence of a physical engraving.
- Cross-group duplicate images are allowed; check for duplicates **within** a group only.
  Detail images are uploaded one at a time with a count check after each; a
  `N not accepted` failure is one-off jitter — re-run the whole card, not the asset.
- Obvious conflicting bank registrations affect only those slots: use the selected
  local file rather than launching a complete old-bank audit.

## Condition, group, company

- Condition: the explicitly confirmed platform enum for that product/batch. Do not
  convert every "factory/original" package label or every copied template to `New`.
- Category and group by product family, not inherited from the template. The group is
  chosen from the store's existing tree; there is no free-text input and no "create
  group" entry. Map the card's label to an existing group explicitly and verify the
  result on the server page; never silently inherit the default group.
- Company intro: preserve a correctly inherited approved company module/card; otherwise
  apply that module once in-product. Never overwrite the shared template.
