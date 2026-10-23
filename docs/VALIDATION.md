# Test and validation record — v0.1

## Implemented checks

Run `python -m unittest discover -s tests -v` after installing the package. These tests check keyword-theme extraction, deterministic composite precedent ranking, geodistance, output constraints, constraint sensitivity, schema error handling and synthetic source notices.

## What these tests do **not** establish

- No live UK planning authority data has been ingested or licensed.
- No genuine historical outcomes have been used to train or calibrate a prediction model.
- There is no evidence of accuracy, calibration, precision/recall, AUROC, Brier score, performance against competitor tools or professional planners, or error rates across councils.
- The demo provides illustrative indices, not true likelihood estimates.
- No consumer usability study or commercial willingness-to-pay test is represented.
- No production security, load or accessibility testing has been undertaken.

## Proposed next independent verification

1. Obtain legally reusable records for two or three pilot local authorities, log provenance and licensing.
2. Define an independent ground-truth sample of historical cases with leakage-resistant chronological splits.
3. Create baseline comparators: majority class, same-proposal-type local historic rate, simple TF-IDF precedent ranker and qualified planner review.
4. Report sample sizes, coverage, balanced accuracy, precision/recall, Brier score, calibration plots and confidence intervals; stratify by authority and proposal class.
5. Record blinded precedent-relevance judgements and inter-rater agreement.
6. Track objection label quality and high-impact false positives/negatives.
7. Add legal/policy signoff and data-refresh checks prior to claiming actionable risk prediction.

Do not describe this repository's unit tests as evidence of a validated planning-prediction model.
