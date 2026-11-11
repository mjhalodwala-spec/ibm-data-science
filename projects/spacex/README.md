# Falcon 9 first-stage landing prediction

## Business question
Estimate whether the first stage lands successfully using launch characteristics that are available before the outcome. This mirrors the stated Applied Data Science Capstone scenario while using a reproducible public API source.

## Workflow
1. Collect launch records from the SpaceX API v4.
2. Retain launches with a first-stage core and a known landing outcome.
3. Derive launch site, payload mass, orbit, booster reuse count and outcome features.
4. Compare a majority-class baseline, logistic regression and random forest with stratified cross-validation.
5. Report precision, recall, F1 and ROC AUC. A final model must be interpreted alongside class balance and data limitations.

## Run

```bash
python -m pip install -e .
python projects/spacex/analyze.py --output reports/spacex
```

The script retrieves data at run time from `https://api.spacexdata.com/v4/launches/query`. API availability and schema can change. It prints cross-validation summaries and saves a CSV of the cleaned analytical table. No scores are preclaimed.

## Limitations
The API is not the course's hosted snapshot. Landing outcome can be affected by missing or revised records, and the model is a retrospective exercise rather than a launch decision system. No causal conclusion follows from feature importance.
