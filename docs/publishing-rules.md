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

## Code consistency (four fields must match the source material's model)

1. OE code - **the platform normalizes away `-`, `&`, `/`...**; compare using the
   normalized value (`AB-120030` = `AB120030`).
2. Engine code - only when the category actually provides the field; record N/A otherwise.
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

## Images and video

- Main images: exactly 5. Detail images: exactly 4, **first one clearly shows the
  model**, four *different* views (same shot with a different logo or crop does not count).
- If the source set has no legible-model image, generate a caption variant ("Model: X"
  in the white margin) with the original preserved and the derivation recorded; never
  fake an engraving.
- Video: the correct non-FST file by exact name; lookalike duplicates are checked by
  cover-image hash. Both main and detail slots must be linked - doing one is not "done".
- Reject assets showing third-party branded packaging (IPR risk).

## Condition, group, company

- Condition: platform enum `New` - not the model code, not a custom spelling.
- Group/category by product family, not inherited from the template.
- Company intro: apply the store's chosen platform template in-product, then swap the
  template's default contact card for the store's own card. Never edit the shared template.
