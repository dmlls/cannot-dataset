Data from the paper **"Not another Negation Benchmark: The NaN-NLI Test Suite
for Sub-clausal Negation" (AACL-ICJNLP 2022)**.

**Source**: https://github.com/joey234/nan-nli

<br>

### Cleaning process

1. Only sentence-pairs classified as `"contradiction"` are kept.
2. From all the columns, only `"premise"` and `"hypothesis"` are kept. These are
   renamed to "sentence" and `"negated"`, respectively.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_nan_nli_data.py original/nan.csv
```
