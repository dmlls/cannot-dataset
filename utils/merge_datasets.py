#!/usr/bin/env python3

"""Merge multiple datasets into a single file."""

import sys
import argparse
from pathlib import Path
from typing import List
import numpy as np

DEFAULT_OUTPUT_DIR = "merged"
OUTPUT_NAME = "negation_dataset"

arg_parser = argparse.ArgumentParser(
    description=("Merge multiple datasets into a single file.")
)
arg_parser.add_argument('datasets', type=argparse.FileType('r'), nargs='+')
arg_parser.add_argument("-s", "--shuffle", action="store_true",
                        help="shuffle the merged data")
arg_parser.add_argument("-i", "--inverse", action="store_true",
                        help="also include the sentence and its negated version "
                             "swapped")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the merged data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


def _swap_sentences(line: str) -> str:
    """Swap a sentence with its negated.

    Args:
        line (:obj:`str`):
            A line in the dataset, in the form::

               r"A sentence.\tThe sentence negated.\n"

    Returns:
        :obj:`str`: The line with the sentences swapped, i.e.::

               r"The sentence negated.\tA sentence.\n"
    """
    sentence, negated = line.strip().split("\t")
    return f"{negated}\t{sentence}\n"


def main(args: argparse.ArgumentParser):
    """Process WikiFactCheck-English dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🖇️  Merging files...")

    lines: List[str] = []
    for dataset in args.datasets:
        for i, line in enumerate(dataset):
            if line not in lines:
                lines.append(line)
            if args.inverse and i != 0:  # don't consider the header
                swapped = _swap_sentences(line)
                if swapped not in lines:
                    lines.append(swapped)

    if args.shuffle:
        header = lines[0]
        lines = np.array(lines[1:])
        np.random.shuffle(lines)
        lines = [header] + lines.tolist()

    with open(output_dir / f"{OUTPUT_NAME}.tsv", "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Done! Output data written to '{output_dir}/'.")


if __name__ == "__main__":
    main(arg_parser.parse_args())
