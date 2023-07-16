Data from the paper [**"It Is Not Easy To Detect Paraphrases: Analysing Semantic
Similarity With Antonyms and Negation Using the New SemAntoNeg
Benchmark"**](https://aclanthology.org/2022.blackboxnlp-1.20/).

**Source**: https://github.com/teemuvh/antonym-substitution

<br>

### Data processing

Each premise is linked to three sentences, from which one of them is a
paraphrased version, and the other two are its negated version (one of them by
adding the negation particle, the other by replacing with an antonym).

We simply label with `1` the negated pairs, and with `0` the paraphrased ones.

No further processing is needed.

<br>

### Running the data processing script

The processed data is already provided under `processed/`. To redo the
processing, simply run:

```Python
python process_antonym_substitution.py original/SemAntoNeg_v1.0.json
```
