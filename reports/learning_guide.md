# Researcher Learning Guide

This guide explains the proposed project. Illustrative examples below are not experimental results.

## What must be understood before training

**Image, lesion and patient are different units.** Several photographs may show one lesion, and several lesions may belong to one patient. Keeping a patient's images together prevents patient overlap. Aggregating photographs per lesion prevents a frequently photographed lesion from dominating primary evaluation.

**A logit is a raw model score.** The classifier produces six scores, one for each diagnosis. Softmax converts them into non-negative probabilities summing to one. The largest probability determines the six-class prediction.

**Accuracy and calibration answer different questions.** Accuracy measures correct decisions. Calibration examines whether confidence agrees with outcomes over repeated predictions. In an illustrative set of predictions near 80% confidence, approximately 80% correct would indicate agreement in that confidence region. One correct or incorrect prediction cannot establish calibration.

**An unconfident model can be wrong, and a confident model can be wrong.** Training loss alone does not show whether the final probabilities are reliable for unseen patients. Evaluation must use held-out data.

## Why four partitions?

| Partition | Question it answers |
|---|---|
| Training | Which weights reduce training loss? |
| Selection validation | Which saved checkpoint should be retained? |
| Calibration validation | Which temperature improves held-out probability quality? |
| Test | How does the complete frozen process perform on untouched patients? |

Reusing test labels to tune any of these choices makes the final evaluation optimistic. Separate selection and calibration subsets make their roles easier to audit, although the small available sample limits precision.

## What each metric tells you

| Metric | Meaning | Caution |
|---|---|---|
| Accuracy | Fraction of correct predictions | Common classes can dominate |
| Balanced accuracy | Mean class recall | Requires explicit class support |
| Macro F1 | Mean class-level F1 | State the fixed class set and undefined cases |
| Sensitivity/recall | Fraction of actual class cases identified | Needs enough positive patients |
| Specificity | Fraction of other-class cases rejected in one-versus-rest analysis | Can look high for a rare class |
| AUROC | Ranking of positives against negatives | Does not measure calibration |
| NLL | Penalty for assigning low probability to the true class | Confident errors receive large penalties |
| Brier | Squared error of the probability vector | State the multiclass normalization |
| ECE | Binned difference between confidence and correctness | Depends on binning and sample size |

## What temperature scaling changes

Dividing all logits by one positive temperature changes probability sharpness while preserving their order. T greater than one softens probabilities; T below one sharpens them. The six-class predicted labels therefore remain the same. Calibration improvement must be measured rather than assumed.

## How to interpret demographic comparisons

Start with support and class composition, not a fairness ranking. A subgroup may contain very few examples of a particular diagnosis. A performance gap may reflect several mechanisms; the study cannot identify a causal explanation from the metric alone. Missing demographics also affect which patients are included in an audit.

Recorded gender is the dataset's field, not automatically verified biological sex. Fitzpatrick skin type is not interchangeable with ethnicity or an objective skin-colour measurement. Do not create missing categories from photographs.

## What the bootstrap can and cannot show

Repeatedly sample patients from the held-out test sample, keeping each patient's lesions together. Recompute metrics on these resamples to describe sampling variability. This does not replace retraining on different seeds or validation in another setting. Narrow intervals also do not repair a biased source sample.

## Questions to answer in a project discussion

1. What is the research question, and what has actually been completed?
2. Why is an image-level random split unsafe for this dataset?
3. Why are checkpoint selection and temperature fitting separate?
4. Why can calibration change while accuracy stays the same?
5. Which demographic fields were actually present and how much was missing?
6. How many independent patients support each main comparison?
7. What did this pilot fail to establish?
8. Which choices and failures were recorded so another researcher could reproduce the work?

Until experiments exist, use planning-stage language such as: “I am developing a patient-separated evaluation pipeline for demographic performance and calibration in skin lesion classification.” Replace it with completed-work language only after implementation and evaluation are complete.
