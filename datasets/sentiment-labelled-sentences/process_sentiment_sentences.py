#!/usr/bin/env python3

"""Process the Sentiment Labelled Sentences dataset for our negation purposes."""

import sys
import argparse
from pathlib import Path
from typing import Optional

import pandas as pd
from negate import Negator

sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # root dir
from src.base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR

arg_parser = argparse.ArgumentParser(
    description=("Process the Sentiment Labelled Sentences Dataset for "
                 "negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the Sentiment Labelled Sentences dataset to "
                             "process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class SentimentSentsDatasetProcessor(BaseDatasetProcessor):
    """Sentiment Labelled Sentences dataset processor.

    See `README.md`.
    """

    def __init__(self, dataset_name: str):
        super().__init__(dataset_name)
        self.negator = Negator(fail_on_unsupported=True)
        # We want to keep only the sentences that contain any of these words.
        self.target_words = [
            "not",
            "I'm", "I am",
            "are", "aren't",
            "he's", "she's", "it's", "is", "isn't",
            "was", "wasn't",
            "were", "weren't",
            "do", "don't",
            "does", "doesn't",
            "did", "didn't",
            "'ve", " haven't",
            "have", "haven't",
            "has", "hasn't",
            "'d", " hadn't",
            "had", "hadn't",
            "can", "can't",
            "could", "couldn't",
            "must", "mustn't",
            "might", "mightn't",
            "may",
            "should", "shouldn't",
            "ought", "oughtn't",
            "'ll", " won't",
            "will", "won't",
            "would", "wouldn't"
        ]

    def _negate_sentence(self, sentence: str) -> Optional[str]:
        try:
            return self.negator.negate_sentence(sentence)
        except RuntimeError:
            print(f"  ⏩ Skipping unsupported sentence: '{sentence}'.")
            return None

    def _process(
        self,
        dataset: str,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        sent_dataset = pd.read_csv(Path(dataset), sep="\t", header=None,
                                   usecols=[0], names=["premise"])
        sent_dataset = sent_dataset.loc[
            sent_dataset["premise"].str.contains("|".join(self.target_words))
        ]
        sent_dataset = sent_dataset[
            sent_dataset["premise"].str.split().str.len().le(33)
        ]
        sent_dataset["hypothesis"] = sent_dataset["premise"].apply(
            self._negate_sentence
        )
        sent_dataset.dropna(inplace=True)  # remove unsupported sentences
        return sent_dataset


def main(args: argparse.ArgumentParser):
    """Process Sentiment Labelled Sentences dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    sents_processor = SentimentSentsDatasetProcessor(
        dataset_name="Sentiment-Labelled-Sentences")
    sents_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
