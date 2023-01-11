Data from the
[**GLUE Diagnostic Dataset**](https://gluebenchmark.com/diagnostics).

**Source**: https://www.dropbox.com/s/ju7d95ifb072q9f/diagnostic-full.tsv?dl=0

<br>

### Cleaning process

1. Only sentence-pairs with label `"contradiction"` are kept.
2. From all the columns, only `"Premise"` and `"Hypothesis"` are kept. These are
   renamed to `"sentence"` and `"negated"`, respectively.
3. Entries in which the `"sentence"` and `"negated"` fields have a Jaccard index
   below `0.55`.
4. Entries in which the `"sentence"` and `"negated"` fields differ in length in
   4 or more words.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_glue_diagnostic_data.py original/nan.csv
```
