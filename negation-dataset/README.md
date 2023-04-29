### Negation Dataset

The version 1.1 of the dataset contains **77376 samples**, of which roughly of
them are negated pairs of sentences, and the other half are not (they are
paraphrased versions of each other).

<br>

The dataset has been created by cleaning up and merging the following datasets:

1. _Not another Negation Benchmark: The NaN-NLI Test Suite for Sub-clausal
Negation_ (see
[`nan-nli`](https://github.com/dmlls/negation-datasets/tree/main/nan-nli)).

2. _GLUE Diagnostic Dataset_ (see
[`glue-diagnostic`](https://github.com/dmlls/negation-datasets/tree/main/glue-diagnostic)).

3. _Automated Fact-Checking of Claims from Wikipedia_ (see
[`glue-diagnostic`](https://github.com/dmlls/negation-datasets/tree/main/wikifactcheck-english)).

4. _From Group to Individual Labels Using Deep Features_ (see
[`sentiment-labelled-sentences`](https://github.com/dmlls/negation-datasets/tree/main/sentiment-labelled-sentences)).
In this case, the negated sentences were obtained by using the Python module
[`negate`](https://github.com/dmlls/negate).


Additionally, for each of the negated samples, another pair of non-negated
sentences has been added by paraphrasing them with the pre-trained model
[`🤗tuner007/pegasus_paraphrase`](https://huggingface.co/tuner007/pegasus_paraphrase).

Finally, the dataset from _It Is Not Easy To Detect Paraphrases: Analysing
Semantic Similarity With Antonyms and Negation Using the New SemAntoNeg
Benchmark_ (see
[`antonym-substitution`](https://github.com/dmlls/negation-datasets/tree/main/antonym-substitution))
has also been included. This dataset already provides both the paraphrased and
negated version for each premise, so no further processing was needed.

<br>

The resulting file is a
[`.tsv`](https://github.com/dmlls/negation-datasets/blob/main/negation-dataset/negation_dataset_v1.1.tsv)
with the following format:

| premise     | hypothesis                              | label |
|:------------|:----------------------------------------|:-----:|
| A sentence. | The sentence non-negated (paraphrased). | 0     |
| A sentence. | The sentence negated.                   | 1     |
