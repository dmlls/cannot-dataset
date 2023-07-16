#!/usr/bin/env python3

"""Produce the final negation dataset.

This script carries out the following steps:

   1. Merge multiple negation datasets.
   2. Add negative cases, i.e., sentences that don't contain any negation. We
      do this automatically using a paraphrasing Transformer model.
   3. Add the column ``label``, which can take two values: ``0`` for
      non-negated pair of sentences, and ``1`` for the negated ones.

The input datasets must be ``.tsv`` files with two columns as follows::

   sentence\tnegated
   First sentence.\tFirst sentence negated.
   Second sentence.\tSecond sentence negated.
   ...

Note that the first line is the header.

The output dataset will also be a ``.tsv`` with three columns, ``premise``,
``hypothesis``, and ``label``, e.g.::

   premise\thypothesis\tlabel
   A sentence.\tThe sentence negated.\t1
   A sentence.\tThe sentence not negated.\t0
   ...

Again, the first line is the header.
"""

import sys
import argparse
from pathlib import Path
from typing import List
import numpy as np
from tqdm import tqdm
import produce_negation_dataset
from paraphrasis import PegasusParaphraser

DEFAULT_OUTPUT_DIR: str = "negation-dataset"
OUTPUT_NAME: str = "negation_dataset"
NON_NEGATED: int = 1

arg_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description=(produce_negation_dataset.__doc__)
)
arg_parser.add_argument('datasets', type=argparse.FileType('r'), nargs='+')
arg_parser.add_argument("-s", "--no-shuffle", action="store_true",
                        help="do not shuffle the data samples")
arg_parser.add_argument("-i", "--no-inverse", action="store_true",
                        help="do not add samples with the premise and the "
                             "hypothesis swapped")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the merged data will be "
                             "written to. If\nnot specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-n", "--non-negated", type=int,
                        default=NON_NEGATED,
                        help="number of non-negated sentences to add per "
                            f"negated\nsentence. Defaults to {NON_NEGATED}.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


def _swap_sentences(line: str) -> str:
    """Swap the premise and hypothesis in a line.

    Args:
        line (:obj:`str`):
            A line in the form::

               r"A sentence.\tThe sentence negated.\t1\n"

    Returns:
        :obj:`str`: The line with the sentences swapped, i.e.::

               r"The sentence negated.\tA sentence.\t1\n"
    """
    sentence, negated, label = line.strip().split("\t")
    return f"{negated}\t{sentence}\t{label}\n"


def main(args: argparse.ArgumentParser):
    """Produce final negation dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n🖇  Merging files...")

    lines: List[str] = []
    for dataset in tqdm(args.datasets):
        contains_label = int("label" in next(dataset))  # header
        for line in dataset:
            line = (line if contains_label
                    else f"{line.strip()}\t1\n")  # add label
            if line not in lines:
                lines.append(line)

    if args.non_negated > 0:
        print("\n⚙  Generating paraphrased sentences...")
        sentences = [line.strip().split("\t")[0] for line in lines]
        batch_size = 32
        batches: List[List[str]] = [
            sentences[i:i+batch_size]
            for i in range(0, len(sentences), batch_size)
        ]
        paraphraser = PegasusParaphraser()
        paraphrased: List[str] = []
        for batch in tqdm(batches):
            paraphrased_batch = paraphraser.paraphrase_batch(
                batch,
                num_return_sentences=args.non_negated
            )
            paraphrased += [
                f"{batch[i]}\t{para_sent}\t0\n"
                for i, paraphrased_sents in enumerate(paraphrased_batch)
                for para_sent in paraphrased_sents
            ]
        lines += paraphrased

    if not args.no_inverse:
        swapped = [_swap_sentences(line) for line in lines]
        swapped = [s for s in swapped if s not in lines]
        lines += swapped

    if not args.no_shuffle:
        lines_np = np.array(lines)
        np.random.default_rng().shuffle(lines_np)
        lines = lines_np.tolist()

    lines = ["premise\thypothesis\tlabel\n"] + lines

    with open(output_dir / f"{OUTPUT_NAME}.tsv", "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\n✅ Done! Output data written to '{output_dir}/'.")


if __name__ == "__main__":
    main(arg_parser.parse_args())
