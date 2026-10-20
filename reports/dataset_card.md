# Dataset Card: PAD-UFES-20 Pilot

Version of this card: 19 October 2026. Scope: locally verified metadata; images not yet inspected.

## Source and licence

- Official release: [PAD-UFES-20 version 1](https://data.mendeley.com/datasets/zr7vgbcyr2/1).
- Dataset DOI: `10.17632/zr7vgbcyr2.1`.
- Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); retain attribution and indicate modifications.
- Associated paper: [Pacheco et al., 2020](https://doi.org/10.1016/j.dib.2020.106221).
- Metadata bytes and checksum: [public source manifest](../configs/data_sources.json).

The release concerns smartphone clinical photographs from a specific Brazilian source population. Broad population or external clinical representativeness has not been established by this project. These are clinical images, not a new dermoscopy collection.

## Locally observed structure

The CSV has 2,298 image records, 26 columns and 1,373 patient identifiers. It contains 1,641 distinct raw lesion IDs and 1,891 patient–lesion pairs. The distinction matters because 250 lesion IDs are reused across patients. The image archive contents and biological lesion identities have not been independently verified.

Use `patient_id` for patient grouping, `(patient_id, lesion_id)` for provisional lesion aggregation, `img_id` to match image files and `diagnostic` as the target. Recorded `age`, `gender` and `fitspatrick` support demographic auditing. `biopsed` describes diagnostic provenance and must not be used as an image-classifier input or target shortcut.

All other inspected columns are: `smoke`, `drink`, `background_father`, `background_mother`, `pesticide`, `skin_cancer_history`, `cancer_history`, `has_piped_water`, `has_sewage_system`, `region`, `diameter_1`, `diameter_2`, `itch`, `grew`, `hurt`, `changed`, `bleed` and `elevation`. The image-only pilot does not use these clinical variables as model inputs.

## Targets and annotation

The six source codes are ACK, BCC, MEL, NEV, SCC and SEK. Consult the original documentation for diagnostic-reference procedures; biopsy status is heterogeneous across labels. This project has not reviewed pathology, relabelled diagnoses or verified clinical correctness.

Class support and diagnostic-reference coverage are reported in the [metadata exploration report](eda_report.md). Image counts, patient–lesion pair counts and patient counts must remain separately labelled.

## Demographic and missing-data handling

- Age disagreements occur for 90 patients and remain unresolved for patient-age summaries.
- Recorded gender and Fitzpatrick type are absent for 579 patients. Their coverage varies strongly with diagnosis.
- Blank and `UNK` entries remain distinct source encodings. The original CSV is never overwritten by cleaning.
- Numeric spellings such as `2` and `2.0` are equivalent in derived numeric demographic summaries.
- A single observed patient attribute can summarise that patient; this does not fill missing source rows. No partly missing patient gender/type records were observed in the accepted release.
- Preserve source gender terminology. Do not equate age, ancestry, gender and Fitzpatrick type with one another or infer missing skin tone from images.
- Positive demographic counts below ten are masked in public figures/tables; suppression does not provide a formal privacy guarantee.

## Permitted project purpose and publication

Academic evaluation of performance and probability quality under the documented pilot protocol. No autonomous diagnosis, treatment recommendation or clinical-safety claim is supported.

Keep raw images, individual metadata, patient-linked split manifests and individual predictions local. Publish only reviewed code, documentation and aggregate results/figures. Never embed raw rows or medical images in public notebook outputs. The public source licence does not remove the need for careful downstream handling.

## Remaining checks

Images must still be acquired, matched to metadata, decoded and checked for duplicated content. Actual splits and supported metrics remain to be determined. The metadata audit does not validate the models, because models have not been trained.
