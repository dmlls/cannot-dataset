### Negation Dataset

This dataset currently contains **60592 samples**, of which half of them are
negated pairs of sentences, and the other half are not (they are paraphrased
versions of each other).

The dataset has been created by cleaning up and merging the following datasets:

* _Not another Negation Benchmark: The NaN-NLI Test Suite for Sub-clausal
Negation_ (see
[`nan-nli`](https://github.com/dmlls/negation-datasets/tree/main/nan-nli))

* _GLUE Diagnostic Dataset_ (see
[`glue-diagnostic`](https://github.com/dmlls/negation-datasets/tree/main/glue-diagnostic))

* _Automated Fact-Checking of Claims from Wikipedia_ (see
[`glue-diagnostic`](https://github.com/dmlls/negation-datasets/tree/main/wikifactcheck-english))

Additionally, for each of the negated samples, another pair of non-negated
sentences has been added by paraphrasing them with the pre-trained model 
[`🤗tuner007/pegasus_paraphrase`](https://huggingface.co/tuner007/pegasus_paraphrase).

The resulting file is a
[`.tsv`](https://github.com/dmlls/negation-datasets/blob/main/negation-dataset/negation_dataset.tsv)
with the following format:

| premise     | hypothesis                              | label |
|:------------|:----------------------------------------|:-----:|
| A sentence. | The sentence non-negated (paraphrased). | 0     |
| A sentence. | The sentence negated.                   | 1     |
