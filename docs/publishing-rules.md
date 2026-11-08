# Listing rules (store policy, generic form)

These encode the store's own compliance and logistics policy. The numbers are the
store's choices; the *shape* of the rules is the reusable part.

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

## Code consistency and actual engine codes

1. OE code - **the platform normalizes away `-`, `&`, `/`...**; compare using the
   normalized value (`AB-120030` = `AB120030`).
2. Engine code - preserve an actual sourced engine code when present; it may differ
   from the part model. Use a model fallback only under the batch's approved rule.
   Record N/A only when the field is genuinely not applicable.
3. Model (attributes) - exact source spelling.
4. Custom attribute "Product name" - pure model code, no decorations.

Plus: SKU/spec fields inherited from the template must be re-checked for the old model.

## MOQ and logistics

- MOQ by real product category: injectors 4, pumps 1, everything else 10 (category of
  the *product*, not of words in the title).
- Lead-time quantity **= MOQ**; lead-time days kept at the approved template value.
- Gross weight (platform field) **= unit weight x MOQ + fixed packaging allowance
  (3 kg)**. Record unit weight, allowance, and computed gross weight separately. Never
  write the single-unit weight; never multiply without the allowance.
- Batch exceptions must bind rule version, batch, actual category and explicit product
  scope together; a weight exception never leaks to every pump.
- Tier prices require their own approved batch basis. A copied tier structure does
  not authorize the inherited price or discount. Compute decimal currency exactly.

## Images and video

- Main images: exactly 5. Detail images: exactly 4, **first one clearly shows the
  model**, four *different* views (same shot with a different logo or crop does not count).
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
- Obvious conflicting bank registrations affect only those slots: use the selected
  local file rather than launching a complete old-bank audit.

## Condition, group, company

- Condition: the explicitly confirmed platform enum for that product/batch. Do not
  convert every "factory/original" package label or every copied template to `New`.
- Group/category by product family, not inherited from the template.
- Company intro: preserve a correctly inherited approved company module/card; otherwise
  apply that module once in-product. Never overwrite the shared template.
