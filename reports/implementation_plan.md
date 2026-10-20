# Implementation Plan and Progress

Updated: 19 October 2026

The project proceeds one phase at a time. Phase 1 supplies research documents only; this checklist does not imply that later code exists.

| Phase | Deliverable | Completion criterion | Status |
|---|---|---|---|
| 1. Research design | Initial literature review, verified sources, pilot protocol | Scope, attribution and outcome definitions documented | Complete as an initial scoping package |
| 2. Data exploration | Metadata audit, dataset card, executed EDA notebook and figures | Metadata schema, supports and missingness verified; image availability/content checks remain a later acquisition gate | Metadata exploration complete; image checks pending |
| 3. Preprocessing | Loader, transforms and patient split | No patient overlap; reproducible assignment; image-label checks pass | Pending |
| 4. Models | CNN and ResNet18 training entry points | Synthetic smoke tests and training-only feasibility checks pass | Pending |
| 5. Performance | Frozen evaluation pipeline | Required metrics verified on synthetic cases, then applied to held-out predictions | Pending |
| 6. Calibration | Temperature fitting and reliability diagrams | Calibration-only fitting and argmax-preservation checks pass | Pending |
| 7. Demographic audit | Supported group metrics and gap plots | Counts, missingness and undefined outcomes handled explicitly | Pending |
| 8. Statistics | Patient-cluster bootstrap comparisons | Resampling multiplicity, pairing and valid replicate counts verified | Pending |
| 9. Figures | Reviewed publication figures | Clear labels, supports, uncertainty and accessible formatting | Pending |
| 10. Report/release | Short report and clean repository | Every result traces to an actual run; no sensitive artifacts included | Pending |

## Completed in Phase 2

1. Retrieve official metadata and record the source version and checksum.
2. Inspect real columns and missing-value encodings before writing transformations.
3. Compare published counts with actual image, lesion and patient counts.
4. Calculate demographic and class supports using correct units.
5. Investigate inconsistent patient records and identifier relationships.
6. Produce aggregate distribution and missingness figures.
7. Decide whether the proposed four-partition design is feasible; record amendments before training.

The audit found 250 reused lesion-ID strings, 90 patients with conflicting ages, and 579 patients without recorded gender/type. The metadata counts and interpretation appear in [eda_report.md](eda_report.md). The four-way split has not been created or declared feasible from achieved split supports.

## Next action: image acquisition and Phase 3

Acquire the official image archives, verify available checksums, check filename coverage and decoding, investigate content duplicates, and then create a patient-separated split. Retain unresolved age status and do not collapse different patients sharing a raw lesion ID.

## Runtime decisions still needed

- Available CPU/GPU or Apple Silicon backend, memory and storage.
- Local versus an approved remote training environment.
- Compatible Python and dependency versions, pinned after verification.
- Training duration measured from a smoke test, not assumed.

Do not upload patient data to a third-party service without checking the dataset conditions and applicable research requirements. Local dataset access alone does not authorise every downstream transfer.

## Reproducibility and release checks

- Use scripts as reproducible entry points and notebooks as explanatory views.
- Add a tested `requirements.txt`, `environment.yml` and installation instructions when implementation exists.
- Test patient separation, lesion aggregation, metrics, temperature fitting and bootstrap behaviour using synthetic fixtures.
- Record code versions and configurations for actual runs.
- Inspect notebook outputs and reports for images and patient-linked rows before publication.
- Allow-list only reviewed aggregate results and figures in Git.
- Keep incomplete report sections explicitly pending; never populate them with literature results or hypothetical numbers.

## Planned final report

The final report will use the 15 requested sections: Abstract, Introduction, Research Question, Related Work, Dataset Description, Methodology, Experimental Setup, Results, Fairness Analysis, Calibration Analysis, Discussion, Limitations, Ethical Considerations, Conclusion and References.

Current status: metadata analysis runs locally and has synthetic correctness tests. Image content and model-training feasibility remain unverified. No model results exist.
