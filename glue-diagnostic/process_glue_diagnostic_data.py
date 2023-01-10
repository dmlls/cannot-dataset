#!/usr/bin/env python3

"""Process the GLUE Diagnostic dataset for our negation purposes."""

import sys
import argparse
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))  # root dir
from base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR

arg_parser = argparse.ArgumentParser(
    description=("Process the GLUE Diagnostic Dataset for negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the GLUE Diagnostic dataset to process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class GlueDiagnosticDatasetProcessor(BaseDatasetProcessor):
    """GLUE Diagnostic dataset processor.

    See `README.md`.
    """

    def _process(
        self,
        dataset: str,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        glue = pd.read_csv(Path(dataset), sep="\t")
        glue = glue.loc[glue["Label"] == "contradiction"]
        glue["Words Different"] = pd.Series.abs(
            glue["Premise"].str.split().str.len()
            - glue["Hypothesis"].str.split().str.len()
        )
        glue = glue.loc[glue["Words Different"] <= 3]
        glue = glue[["Premise", "Hypothesis"]]
        glue.rename(columns={"Premise": "sentence",
                             "Hypothesis": "negated"},
                    inplace=True)
        return glue


def main(args: argparse.ArgumentParser):
    """Process GLUE Diagnostic dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    glue_diagnostic_processor = GlueDiagnosticDatasetProcessor(
        dataset_name="GLUE Diagnostic")
    glue_diagnostic_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
