# Housing price regression brief

A leakage-conscious regression exercise: reserve a holdout set before fitting transformations, impute missing values inside a pipeline, encode categoricals, compare a median baseline with linear and tree models, and inspect residuals by price range. Use a licensed public housing dataset supplied locally as CSV and choose the label explicitly.

```bash
python model.py data/housing.csv --target median_house_value
```

This repository does not bundle a dataset or imply a result. Housing data is geographically and temporally specific; do not treat an average prediction as a property appraisal.
