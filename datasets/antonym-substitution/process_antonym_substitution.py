#!/usr/bin/env python3

"""Process the SemAntoNeg dataset for our negation purposes."""

import sys
import argparse
import json
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # root dir
from src.base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR

arg_parser = argparse.ArgumentParser(
    description=("Process the SemAntoNeg Dataset for negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the SemAntoNeg dataset to process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class SemAntoNegDatasetProcessor(BaseDatasetProcessor):
    """SemAntoNeg dataset processor.

    See `README.md`.
    """

    def _process(
        self,
        dataset: str,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        with open(Path(dataset), "r", encoding="utf-8") as f:
            sem_anto_neg = [json.loads(line) for line in f if line.strip()]
        sem_anto_neg = [
            {
                "premise": sample["input"],
                "hypothesis": sentence,
                "label": int(i != int(sample["label"])),
            }
            for sample in sem_anto_neg
            for i, sentence in enumerate(sample["sentences"])
        ]
        return pd.DataFrame(sem_anto_neg).drop_duplicates()


def main(args: argparse.ArgumentParser):
    """Process SemAntoNeg dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    sem_anto_neg_processor = SemAntoNegDatasetProcessor(dataset_name="SemAntoNeg")
    sem_anto_neg_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
