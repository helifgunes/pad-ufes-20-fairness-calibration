# pad-ufes-20-fairness-calibration
Fairness and calibration evaluation of a skin lesion classifier on PAD-UFES-20

An individual pilot research project using PAD-UFES-20 to compare a small CNN trained from scratch with an ImageNet-pretrained ResNet18.

**Status: Phase 1 research documentation is complete. Data inspection, code implementation, model training and experimental evaluation are pending. No project results are available yet.**

## Research question

How do a CNN trained from scratch and a pretrained ResNet18 differ in six-class classification performance and probability calibration across recorded gender and predefined age groups in PAD-UFES-20, and how does global temperature scaling affect overall and subgroup calibration?

## Start here

1. [Research protocol](reports/protocol.md): the experimental design and interpretation rules.
2. [Initial literature review](reports/literature_review.md): verified sources, findings and the proposed contribution.
3. [Learning guide](reports/learning_guide.md): concepts to understand before implementing the project.
4. [Implementation plan](reports/implementation_plan.md): the next phases and completion criteria.
5. [Source register](reports/source_register.md) and [BibTeX bibliography](reports/references.bib).
6. [Data access instructions](data/README.md).

## Pilot scope

- Image-only models; demographic metadata is reserved for subgroup evaluation.
- One frozen patient-separated split with distinct training, model-selection validation, calibration validation and test partitions.
- One training seed per model. Cross-validation and repeated seeds are future extensions.
- Primary evaluation at lesion level, with patient-cluster bootstrap uncertainty.
- Performance, probability-quality and subgroup comparisons.
- No clinical deployment or claim of validated performance outside the source population.

The initial scope is deliberately limited. A single split and seed cannot establish robustness to split or training variability. Comparing two different architectures also does not isolate the effect of pretraining.

## Repository structure

```text
configs/       Prospective study specification
data/          Access instructions; local medical data remains ignored
notebooks/     Exploratory notebooks will follow in Phase 2
src/           Modular implementation will follow in later phases
scripts/       Reproducible entry points will follow implementation
tests/         Correctness and leakage tests will follow implementation
results/       Reviewed aggregate tables only
figures/       Reviewed aggregate figures only
reports/       Protocol, literature review, references and learning notes
```

## Installation and execution

Phase 1 is documentation only. There is no runnable training pipeline yet. Pinned requirements, an environment definition and tested run commands will be added after the data audit and runtime inspection. No commands for nonexistent scripts are presented as executable.

## Reproducibility

Future experiments will record dataset checksums, split settings, resolved configurations, random seeds, dependency versions, pretrained-weight identifiers, hardware and the code revision. Individual split assignments and predictions remain local.

## Publication and ethics

Do not commit medical images, individual metadata, patient identifiers, patient-linked predictions or model checkpoints. The ignore rules protect common paths and formats, but cannot inspect notebook cells or report text. Review every publication file for patient information and sparse-cell disclosure.

Dataset licensing is separate from licensing this project's code. The official dataset uses CC BY 4.0; preserve attribution, link the licence and indicate modifications. A project code licence has not yet been selected.

This project is academic research. Calibration, high accuracy or similar group metrics do not establish clinical safety or universal fairness.

## Evidence status

| Activity | Status |
|---|---|
| Official documentation checked | Completed |
| Initial targeted literature review | Completed; not a systematic review |
| Prospective pilot protocol | Completed, subject to data-feasibility checks |
| Local metadata and image audit | Pending |
| Model implementation and training | Pending |
| Calibration and subgroup evaluation | Pending |
| Experimental report | Pending |

Only describe work as completed when its corresponding artifacts exist. Researcher review and understanding of AI-assisted material are required; document assistance according to applicable university requirements.
