#!/usr/bin/env python3

"""Process the NaN-NLI dataset for our negation purposes."""

import sys
import argparse
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))  # root dir
from base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR

arg_parser = argparse.ArgumentParser(
    description=("Process the NaN-NLI Dataset for negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the NaN-NLI dataset to process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class NanNliDatasetProcessor(BaseDatasetProcessor):
    """NaN-NLI dataset processor.

    See `README.md`.
    """

    def _process(
        self,
        dataset: str,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        nan_nli = pd.read_csv(Path(dataset), sep=",")
        nan_nli = nan_nli.loc[nan_nli["label"] == "contradiction"]
        nan_nli = nan_nli[["premise", "hypothesis"]]
        nan_nli.rename(columns={"premise": "sentence",
                                "hypothesis": "negated"},
                       inplace=True)
        return nan_nli


def main(args: argparse.ArgumentParser):
    """Process NaN-NLI dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    nan_nli_processor = NanNliDatasetProcessor(dataset_name="NaN-NLI")
    nan_nli_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
