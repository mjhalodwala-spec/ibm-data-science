# Loan repayment classification brief

Build a classifier for whether an anonymized loan is repaid. Keep the target separate from all input columns, split before preprocessing, compare a simple baseline with logistic regression and a tree ensemble, and report precision/recall alongside ROC AUC. Select a decision threshold against the relative costs of missed defaults and unnecessary review. Do not describe the output as a credit decision or use it to screen real applicants.

**Data:** provide a lawful, de-identified tabular dataset as `data/loans.csv`; set the target column with `--target`. The script refuses to guess a target. No personal data is included in this repository.
