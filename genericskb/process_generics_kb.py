#!/usr/bin/env python3

"""Process the GenericsKB dataset for our negation purposes."""

import sys
import argparse
from pathlib import Path
from typing import Optional

import pandas as pd
from negate import Negator

sys.path.insert(0, str(Path(__file__).parent.parent))  # root dir
from base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR

arg_parser = argparse.ArgumentParser(
    description=("Process the GenericsKB Dataset for negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the GenericsKB dataset to process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class GenericsKBDatasetProcessor(BaseDatasetProcessor):
    """GenericsKB dataset processor.

    See `README.md`.
    """

    def __init__(self, dataset_name: str):
        super().__init__(dataset_name)
        self.negator = Negator(fail_on_unsupported=True)

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
        kb_dataset = pd.read_csv(Path(dataset), sep="\t", usecols=[3], header=0,
                                 names=["premise"])
        kb_dataset = kb_dataset[
            kb_dataset["premise"].str.split().str.len().le(33)
        ]
        kb_dataset["hypothesis"] = kb_dataset["premise"].apply(
            self._negate_sentence
        )
        kb_dataset.dropna(inplace=True)  # remove unsupported sentences
        return kb_dataset


def main(args: argparse.ArgumentParser):
    """Process GenericsKB dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    kb_processor = GenericsKBDatasetProcessor(dataset_name="GenericsKB")
    kb_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
