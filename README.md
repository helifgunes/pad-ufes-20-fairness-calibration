# pad-ufes-20-fairness-calibration
Fairness and calibration evaluation of a skin lesion classifier on PAD-UFES-20

An individual pilot research project using PAD-UFES-20 to compare a small CNN trained from scratch with an ImageNet-pretrained ResNet18.

**Status: Phase 1 documentation and Phase 2 metadata exploration are complete. The official CSV has been verified, audited and visualised. Image-content checks, patient splitting, model training and predictive/calibration evaluation are pending. There are no model results yet.**

The metadata audit found reused lesion IDs, conflicting ages for 90 patients and missing gender/type information for 579 patients. Read the [observed metadata findings](reports/eda_report.md) before training.

## Research question

How do a CNN trained from scratch and a pretrained ResNet18 differ in six-class classification performance and probability calibration across recorded gender and predefined age groups in PAD-UFES-20, and how does global temperature scaling affect overall and subgroup calibration?

## Start here

1. [Research protocol](reports/protocol.md): the experimental design and interpretation rules.
2. [Initial literature review](reports/literature_review.md): verified sources, findings and the proposed contribution.
3. [Learning guide](reports/learning_guide.md): concepts to understand before implementing the project.
4. [Implementation plan](reports/implementation_plan.md): the next phases and completion criteria.
5. [Source register](reports/source_register.md) and [BibTeX bibliography](reports/references.bib).
6. [Data access instructions](data/README.md).
7. [Executed exploration notebook](notebooks/01_dataset_exploration.ipynb) and [dataset card](reports/dataset_card.md).

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
configs/       Prospective study specification and verified source manifest
data/          Access instructions; local medical data remains ignored
notebooks/     Executed metadata exploration; aggregate outputs only
src/data/      Metadata validation, counting and aggregate figures
scripts/       Verified metadata import and audit entry points
tests/         Synthetic metadata correctness tests; model tests will follow
results/       Reviewed aggregate tables only
figures/       Reviewed aggregate figures only
reports/       Protocol, literature review, references and learning notes
```

## Installation and execution

Use Python 3.12. These dependencies support metadata exploration, not model training.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/download_metadata.py
```

If the official host blocks direct HTTP downloading, download `metadata.csv` through its [file page](https://data.mendeley.com/datasets/zr7vgbcyr2/1/files/fa850265-57da-48f0-ba3e-998b3e44b1f6), then import it with checksum verification:

```bash
python scripts/download_metadata.py --from-file /path/to/downloaded/metadata.csv
python scripts/audit_data.py
python -m pytest -q
```

The audit creates `results/metadata_audit.json` and six aggregate plots in both SVG and PNG under `figures/eda/`. No patient rows or medical photographs are exported. To use Conda, run `conda env create -f environment.yml` from the repository root. `requirements-lock.txt` records the tested Python 3.12 macOS arm64 environment; the Conda recipe has not been separately executed.

Open the notebook in a Python environment with `ipykernel` installed. Training, split generation and calibration fitting commands will be added when those phases exist.

## Reproducibility

The metadata audit records the official file checksum and source-code fingerprints. Dependency versions are pinned and the analysis unit is explicit. Future model experiments will also record split settings, resolved configurations, random seeds, pretrained-weight identifiers, hardware and the code revision. Individual split assignments and predictions remain local.

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
| Local metadata audit and six EDA plots | Completed; see the metadata report |
| Image-content and availability checks | Pending |
| Synthetic metadata tests | Implemented and passing |
| Model implementation and training | Pending |
| Calibration and subgroup evaluation | Pending |
| Experimental report | Pending |

Only describe work as completed when its corresponding artifacts exist. Researcher review and understanding of AI-assisted material are required; document assistance according to applicable university requirements.
