<p align="center"><img width="500" src="https://github.com/dmlls/cannot-dataset/assets/22967053/a380dfdf-3514-4771-90c4-636698d5043d" alt="CANNOT dataset"></p>
<p align="center" display="inline-block">
  <a href="https://github.com/dmlls/cannot-dataset/">
    <img src="https://img.shields.io/badge/version-1.1-green">
  </a>
</p>
<h2 align="center">Compilation of ANnotated, Negation-Oriented Text-pairs</h2>

<br><br>

## Introduction

**CANNOT** is a dataset that focuses on negated textual pairs. It currently
contains **77,376 samples**, of which roughly of them are negated pairs of
sentences, and the other half are not (they are paraphrased versions of each
other).

The most frequent negation that appears in the dataset is verbal negation (e.g.,
will → won't), although it also contains pairs with antonyms (cold → hot).

<br>

## Format

The dataset is given as a
[`.tsv`](https://en.wikipedia.org/wiki/Tab-separated_values) file with the
following structure:

| premise     | hypothesis                                         | label |
|:------------|:---------------------------------------------------|:-----:|
| A sentence. | An equivalent, non-negated sentence (paraphrased). | 0     |
| A sentence. | The sentence negated.                              | 1     |

<br>

The dataset can be easily loaded into a Pandas DataFrame by running:

```Python
import pandas as pd

dataset = pd.read_csv('negation_dataset_v1.0.tsv', sep='\t')

```

<br>

## Construction

The dataset has been created by cleaning up and merging the following datasets:

1. _Not another Negation Benchmark: The NaN-NLI Test Suite for Sub-clausal
    Negation_ (see
[`datasets/nan-nli`](https://github.com/dmlls/cannot-dataset/tree/main/datasets/nan-nli)).

2. _GLUE Diagnostic Dataset_ (see
[`datasets/glue-diagnostic`](https://github.com/dmlls/cannot-dataset/tree/main/datasets/glue-diagnostic)).

3. _Automated Fact-Checking of Claims from Wikipedia_ (see
[`datasets/wikifactcheck-english`](https://github.com/dmlls/cannot-dataset/tree/main/datasets/wikifactcheck-english)).

4. _From Group to Individual Labels Using Deep Features_ (see
[`datasets/sentiment-labelled-sentences`](https://github.com/dmlls/cannot-dataset/tree/main/datasets/sentiment-labelled-sentences)).
In this case, the negated sentences were obtained by using the Python module
[`negate`](https://github.com/dmlls/negate).

5. _It Is Not Easy To Detect Paraphrases: Analysing Semantic Similarity With
Antonyms and Negation Using the New SemAntoNeg Benchmark_ (see
[`datasets/antonym-substitution`](https://github.com/dmlls/cannot-dataset/tree/main/datasets/antonym-substitution)).

<br>

Once processed, the number of remaining samples in each of the datasets above are:

| Dataset                                                                   | Samples    |
|:--------------------------------------------------------------------------|-----------:|
| Not another Negation Benchmark                                            |      118   |
| GLUE Diagnostic Dataset                                                   |      154   |
| Automated Fact-Checking of Claims from Wikipedia                          |   14,970   |
| From Group to Individual Labels Using Deep Features                       |    2,110   |
| It Is Not Easy To Detect Paraphrases                                      |    8,597   |
| <div align="right"><b>Total</b></div>                                     | **25,949** |

<br>

Additionally, for each of the negated samples, another pair of non-negated
sentences has been added by paraphrasing them with the pre-trained model
[`🤗tuner007/pegasus_paraphrase`](https://huggingface.co/tuner007/pegasus_paraphrase).

Finally, the swapped version of each pair (premise ⇋ hypothesis) has also been
included, and any duplicates have been removed.

With this, the number of premises/hypothesis in the CANNOT dataset that appear
in the original datasets are:

| <div align="left"><b>Dataset</b></div>                                                                   | <div align="center"><b>Sentences</b></div>             |
|:--------------------------------------------------------------------------|----------------------:|
| Not another Negation Benchmark                                            |         552 &nbsp;&nbsp;&nbsp; (0.36 %) |
| GLUE Diagnostic Dataset                                                   |         586 &nbsp;&nbsp;&nbsp; (0.38 %) |
| Automated Fact-Checking of Claims from Wikipedia                          |      89,728 &nbsp; (59.98 %) |
| From Group to Individual Labels Using Deep Features                       |      12,626 &nbsp;&nbsp;&nbsp; (8.16 %) |
| It Is Not Easy To Detect Paraphrases                                      |      17,198 &nbsp; (11.11 %) |
| <div align="right"><b>Total</b></div>                                     | **120,690** &nbsp; (77.99 %) |

The percentages above are in relation to the total number of premises and
hypothesis in the CANNOT dataset. The remaining 22.01 % (34,062 sentences) are
the novel premises/hypothesis added through paraphrase and rule-based negation.

<br>

## Contributions

Questions? Bugs...? Then feel free to [open a new
issue](https://github.com/dmlls/cannot-dataset/issues/new/).

<br>

## Acknowledgments

We thank all the previous authors that have made this dataset possible:

Thinh Hung Truong, Yulia Otmakhova, Timothy Baldwin, Trevor Cohn, Jey Han Lau,
Karin Verspoor, Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer
Levy, Samuel R. Bowman, Aalok Sathe, Salar Ather, Tuan Manh Le, Nathan Perry,
Joonsuk Park, Dimitrios Kotzias, Misha Denil, Nando De Freitas, Padhraic Smyth,
Teemu Vahtola, Mathias Creutz, and Jörg Tiedemann.

<br>

## License

The CANNOT dataset is released under [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/).

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
    <img alt="Creative Commons License" width="100px" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png"/>
</a>

<br><br>

## Citation
```bibtex
@misc{anschütz2023correct,
      title={This is not correct! Negation-aware Evaluation of Language Generation Systems}, 
      author={Miriam Anschütz and Diego Miguel Lozano and Georg Groh},
      year={2023},
      eprint={2307.13989},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
