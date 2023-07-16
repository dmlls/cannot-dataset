Data from the paper [**"From Group to Individual Labels Using Deep
Features"**](https://dkotzias.com/papers/GICF.pdf).

**Source**:
https://www.kaggle.com/datasets/marklvl/sentiment-labelled-sentences-data-set

<br>

### Cleaning process

1. Manually correct typos and formatting issues (files appended with
   "-corrected").
2. Remove the label column.
3. Keep only sentences that contain auxiliary verbs and have at most 33 words.
4. For each sentence, run the Python "[negate](https://github.com/dmlls/negate)"
   module to get its negated version. Non-supported sentences are removed.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_sentiment_sentences.py original/imdb_labelled-corrected.txt
```
