# Initial Literature Review

Review date: 16 October 2026

This is a targeted scoping review to guide a small individual project. It is not a systematic review or a claim that all relevant studies have been found. Entries distinguish what the source establishes from implications for this project. Some entries are based on abstracts; they are not full methodological replications.

## Search approach

Searches combined PAD-UFES-20, skin lesion classification, demographic fairness, probability calibration, temperature scaling, patient separation and reliability. Foundational papers were also checked by title. Examples of queries used:

- `PAD-UFES-20 demographic fairness probability calibration temperature scaling skin lesion classification`
- `skin lesion classification demographic disparities calibration patient split reliability`
- `medical imaging fairness calibration subgroup evaluation`

Use publisher pages, conference proceedings and author manuscripts as primary evidence. Search snippets and secondary descriptions are discovery aids, not authoritative definitions of dataset properties. Prefer sources that directly inform data provenance, classification, fairness, calibration or attribute interpretation. The source register records verification scope.

## Evidence matrix

| Study | Finding supported by the checked source | Relevance and limits for this project |
|---|---|---|
| [Pacheco et al., 2020](https://arxiv.org/html/2007.00478) | Defines the smartphone clinical-image dataset, metadata and diagnostic-reference process. Reports severe class imbalance, including only 52 melanoma images. | Establishes the data hierarchy and motivates careful support reporting. Published image counts are not independent patient counts. Local auditing is still required. |
| [Esteva et al., 2017](https://www.nature.com/articles/nature21056) | Demonstrates strong CNN performance against dermatologists in specified image-based classification tasks. | Establishes feasibility of image-based learning. The evaluated tasks do not establish this project's demographic fairness, calibration or clinical utility. |
| [Guo et al., 2017](https://proceedings.mlr.press/v70/guo17a.html) | Finds miscalibration in modern networks and demonstrates effective single-parameter temperature scaling on studied datasets. | Motivates a simple calibration baseline. Improvement on PAD-UFES-20 or within every group is an empirical question, not a guaranteed outcome. |
| [Daneshjou et al., 2022](https://arxiv.org/abs/2203.08807) | Evaluates dermatology models on a curated, diverse clinical-image dataset and identifies limitations across skin tones and uncommon diseases. | Motivates subgroup and generalisation auditing. Results on DDI cannot be transferred directly to the PAD-UFES-20 sample or interpreted using invented skin-tone labels. |
| [Vaicenavicius et al., 2019](https://proceedings.mlr.press/v89/vaicenavicius19a.html) | Develops a theoretical framework for evaluating probabilistic calibration and discusses subtleties in existing evaluations. | Supports precise metric definitions and qualified interpretation. A single binned top-label score does not establish every aspect of multiclass calibration. |
| [Pleiss et al., 2017](https://arxiv.org/abs/1709.02012) | Investigates tensions between calibrated probabilities and group error constraints under its formal setting. | Motivates multiple, explicitly defined fairness measures. Its theoretical results must not be restated as a universal impossibility theorem for this six-class dataset. |
| [Groh et al., 2022](https://arxiv.org/abs/2207.02942) | Examines human and algorithmic Fitzpatrick annotations and distinguishes photosensitivity from its use as an estimated skin-tone proxy. | Motivates cautious interpretation of recorded Fitzpatrick types. This does not validate PAD-UFES-20 annotations or justify estimating missing types from images. |
| [Rocha and Krohling, 2026](https://link.springer.com/article/10.1007/s41666-026-00252-w) | Benchmarks bias-mitigation approaches using multimodal-derived tabular representations, including PAD-UFES-20. | Direct evidence that fairness research on this dataset already exists. Its different task and sample processing prevent direct comparison of headline results without protocol alignment. |
| [Shui et al., 2023](https://arxiv.org/abs/2307.01738) | Investigates subgroup calibration bias with Cluster-Focal, including experiments on HAM10000 and an MS application. | Direct prior work at the intersection of calibration and medical-imaging fairness. Our contribution is a smaller, transparent pilot audit, not the invention of subgroup calibration analysis. |

## Synthesis

Three questions should remain separate: whether predictions discriminate classes, whether probabilities match outcomes, and whether these properties differ across groups. Each answers a different research question. The pilot will therefore report classification metrics alongside probability scores and reliability diagrams, then examine the same quantities within recorded groups.

The literature supports caution about transferring results between datasets. Image modality, label definitions, disease distribution and subgroup annotation can differ. External validation requires a separate compatible protocol; a random holdout within one source population is not external validation.

The small pilot should measure differences rather than optimise a fairness target. It will use one global temperature, not demographic-specific post-processing. This makes the before/after analysis easy to inspect but does not imply that every subgroup benefits. The design also avoids conflating a change in confidence with a change in six-class decisions.

## Defensible contribution

The proposed contribution is an educational, reproducible pilot evaluating classification and subgroup probability quality together on PAD-UFES-20, with explicit patient separation, lesion aggregation, missing-data coverage, support counts and conditional uncertainty intervals.

This is not evidence of a previously unstudied research gap. The gap is a project-level evaluation need: producing an inspectable implementation and a qualified analysis under a clearly documented protocol. The novelty of any stronger claim would require a broader full-text review.

## Remaining review work

- Read full methods before reproducing another study's split, fairness definition or numerical comparison.
- Extract patient separation, analysis unit, calibration data use and uncertainty methods from closely related full texts.
- Add newly relevant studies with verification scope and access date.
- Do not copy results from the literature into this project's results tables.

The initial review is complete as a scoping deliverable. It remains updateable as implementation exposes more specific questions.
