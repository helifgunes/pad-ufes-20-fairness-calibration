# Pilot Research Protocol

Version: 0.1 — 16 October 2026

Status: prospective. No local dataset audit, training or experimental evaluation has been performed. This is a local protocol, not an externally registered preregistration.

## Question and contribution

How do a CNN trained from scratch and an ImageNet-pretrained ResNet18 differ in six-class performance and probability calibration across recorded gender and predefined age groups in PAD-UFES-20, and how does global temperature scaling affect overall and subgroup calibration?

The intended contribution is a reproducible pilot audit combining discrimination, subgroup probability quality, leakage prevention and uncertainty. Prior work already investigates demographic fairness and calibration; no first-study or new-algorithm claim is made. See the [literature review](literature_review.md).

The study describes associations within the available sample. It cannot establish demographic causation, clinical safety or performance in all populations.

## Data audit gate

Use the [official version 1 release](https://data.mendeley.com/datasets/zr7vgbcyr2/1). The release reports 2,298 images, 1,641 lesions and 1,373 patients. These are published reference values, not locally verified counts.

The documented target labels are ACK, BCC, MEL, NEV, SCC and SEK. Relevant fields include `patient_id`, `lesion_id`, `img_id`, `diagnostic`, `age`, `gender`, `fitspatrick` and `biopsed`. The misspelled `fitspatrick` field name is retained. Blank values and `UNK` need explicit handling. [Dataset documentation](https://arxiv.org/html/2007.00478)

Audit actual columns, labels, unique IDs, readable images, duplicates, patient-to-lesion relationships, conflicting records and missing metadata. Use `(patient_id, lesion_id)` as the lesion key unless global uniqueness is verified. Identical or near-identical images with different patient IDs require investigation before splitting; keep connected records together or exclude unresolved records using a documented rule.

Retain records with missing audit attributes in overall image-only evaluation where other eligibility requirements are met. Report missing/unknown categories separately. Do not infer demographics from images, invent values, equate ancestry with verified ethnicity or silently choose the first conflicting demographic record.

## Evaluation design

The time-limited pilot uses one patient-separated split and one training seed per model. This replaces the earlier five-fold, three-seed proposal before any experimental outcomes are known.

| Partition | Target share of patients | Purpose |
|---|---:|---|
| Training | 60% | Model updates and training-only statistics |
| Selection validation | 10% | Checkpoint selection and declared development choices |
| Calibration validation | 10% | Temperature fitting after model selection |
| Test | 20% | Final frozen-pipeline evaluation |

Split seed: 42. Approximate diagnosis stratification should consider each patient's collection of lesion labels; patients may have multiple diagnoses. Prioritise zero patient overlap over exact ratios. Review support using metadata, never model outcomes. If rare-class patient support makes the design infeasible, amend the protocol and record the reason before training.

Save assignments locally with their checksum, algorithm and achieved counts. Freeze the final split and recipes before test evaluation. Report both prespecified models. If test outcomes influence later choices, disclose the contamination and require fresh evaluation for confirmatory claims.

## Evaluation unit

Train on images. For primary evaluation, average image logits within each lesion and then compute probabilities. Fit temperature using the same lesion-logit aggregation on calibration-validation lesions. Each lesion contributes once to primary metrics.

Report image-level metrics secondarily with the same temperature and identify them as secondary; the temperature has not been separately fitted for the image-level distribution. Demographic summaries count unique patients. Bootstrap resampling keeps all lesions from a patient together.

## Prospective models and preprocessing

- Small CNN: three convolutional blocks, pooling, global average pooling and a six-logit head; random initialization.
- ResNet18: ImageNet-pretrained weights and a replacement six-logit head; fine-tune all layers and record the exact weight identifier.

These approaches differ in architecture and initialization. Their comparison cannot isolate the effect of pretraining.

Initial preprocessing: RGB conversion; aspect-ratio-preserving resizing of the longest side to 224 pixels and padding to 224 by 224; documented ImageNet channel normalization for both models. Training augmentation: independent horizontal and vertical flips, each with probability 0.5. No random augmentation for validation or test. Inspect image coverage and padding before implementation is frozen.

Initial recipes: unweighted cross-entropy, AdamW, batch size 32, weight decay 0.0001, maximum 30 epochs and early-stopping patience 5. Initial learning rates: 0.001 for CNN and 0.0001 for ResNet18. Select the checkpoint with lowest lesion-level selection-validation NLL, breaking ties by earlier epoch. Record any engineering changes before final runs.

Seed Python, NumPy, PyTorch and loader workers with 42. Log backend determinism settings and limitations; do not promise identical floating-point results across devices. Hardware feasibility checks use training data, not test outcomes.

Class imbalance is handled initially through balanced and per-class reporting. A training-count-derived weighted-loss experiment is a future extension. Never rebalance validation or test sets.

## Metrics

Primary predictive summary: lesion-level macro F1. Also report accuracy, balanced accuracy, per-class precision, recall/sensitivity, one-versus-rest specificity, AUROC where defined and confusion matrices with supports.

Keep a fixed six-class definition for macro summaries. If a metric cannot be evaluated across all classes because a class is unsupported, mark the six-class summary unavailable. A separately named supported-class summary must not be presented as equivalent. Undefined values are not silently changed to zero; zero recall for an actually present but entirely missed class is valid.

Primary probability-quality comparison: calibrated minus uncalibrated NLL for each model; negative values indicate improvement. NLL and Brier are proper probability scores, not pure calibration measures.

For N lesions and K=6 classes:

- NLL: `-mean(log(p[i, y[i]]))`, computed stably from logits.
- Multiclass Brier: `mean(sum_k((p[i,k] - one_hot(y[i])[k])**2))`, without division by K; range 0 to 2.
- Top-label ECE: `sum_b(n_b/N * abs(mean_correct_b - mean_confidence_b))`.

Use ten fixed equal-width bins `[0,0.1)`, ..., `[0.9,1.0]`. Empty bins contribute nothing; display bin supports in reliability diagrams. Five- and fifteen-bin sensitivity analyses are exploratory. Top-label ECE does not establish full multiclass calibration. Plot classwise reliability only where supported.

## Temperature scaling

Use `softmax(z/T)` with positive T, parameterised through log T. Freeze network weights and minimise unweighted lesion-level NLL on calibration-validation data only. Record optimiser settings, convergence, bounds if used and any boundary solution. Do not fit subgroup-specific temperatures in the pilot.

If fitting fails, report failure rather than presenting T=1 as a successfully fitted result. Test data must not determine T or the calibration method.

Evaluate identical test lesions before and after scaling. A shared positive temperature preserves six-class argmax labels, so hard classification metrics should remain unchanged. Probability-quality metrics can improve or worsen overall and within subgroups. Global improvement does not establish subgroup improvement.

## Demographic analysis

- Age: under 60 versus 60 and over. This is a declared study convention, not a biological boundary. Missing, invalid or unresolved ages are separate.
- Gender: retain observed categories and call the field recorded `gender`, not verified biological sex. Unknown/missing/unresolved records are explicit.
- Fitzpatrick: exploratory type-specific summaries, conditional on support. Do not infer types from images or equate the scale with objectively measured skin colour. Do not merge categories after seeing outcomes.

Core outcomes by group: accuracy, per-class sensitivity/specificity, NLL, Brier and ECE. Include patient, lesion and image counts, class composition and missingness coverage.

For age, signed gaps are older minus younger. If two known gender categories occur, use a documented alphabetical order for signed comparisons. With additional categories, report supported pairwise comparisons as exploratory. Before/after changes are after minus before. Intersectional and ancestry-based evaluation are outside the core pilot.

Flag groups with fewer than 30 patients and class-specific rates with fewer than 10 contributing positive/negative patients. These are display warnings, not validated power thresholds. Larger groups can also be uncertain. Keep undefined metrics explicit; do not rank sparse groups or make definitive fairness verdicts. Review sparse cells before public release.

Observed gaps may reflect case mix, prevalence, acquisition, diagnostic-reference differences or selection. Similar accuracy does not prove fairness; a gap does not establish a causal demographic effect.

## Statistical uncertainty

Use 2,000 patient-cluster bootstrap replicates with seed 2026. Sample test patient IDs with replacement and retain all lesions for each sampled patient, including repeated multiplicity. Use the same resamples for paired model differences, calibration changes and group-gap comparisons.

Report percentile 95% intervals using 2.5th and 97.5th percentiles. Retain undefined replicates as undefined and disclose valid replicate counts. Suppress an interval if fewer than 95% of requested replicates are valid; retain a defined point estimate with its warning.

These intervals are conditional on this split and fitted models; they do not capture training, split-selection or temperature-refitting variability. A zero-spanning interval does not establish equivalence. No primary significance test is planned. Multiple exploratory comparisons are not confirmatory discoveries.

## Reporting and limitations

Produce training curves, performance comparisons, confusion matrices, reliability diagrams, subgroup comparisons and gap plots. Use accessible colours, readable labels, supports and intervals; export vector graphics or high-resolution raster figures.

The final report will contain: Abstract; Introduction; Research Question; Related Work; Dataset Description; Methodology; Experimental Setup; Results; Fairness Analysis; Calibration Analysis; Discussion; Limitations; Ethical Considerations; Conclusion; References. Pending experiments remain marked pending.

Limitations: one source population, rare classes and groups, incomplete metadata, differing diagnostic references, one split, one seed, ECE bin dependence, conditional uncertainty and no external validation. Patient holdout estimates generalisation to unseen patients from this source, not to other clinical settings.

Future work: repeated seeds, grouped cross-validation, randomly initialised ResNet18, weighted-loss ablation, calibration-refitting uncertainty and appropriately licensed external validation. These remain proposals.

## Change log

| Date | Change | Reason | Test outcomes available? |
|---|---|---|---|
| 2026-10-16 | Initial pilot protocol: one split and one seed replace the larger proposal | Time-limited individual research project | No |
