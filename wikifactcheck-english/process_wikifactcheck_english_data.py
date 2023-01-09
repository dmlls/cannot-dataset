#!/usr/bin/env python3

"""Process the WikiFactCheck-English dataset for our negation purposes."""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
import spacy
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent))  # root dir
from base_dataset_processor import BaseDatasetProcessor, DEFAULT_OUTPUT_DIR
from utils.jaccard_index import jaccard_similarity
from utils.text_processing import add_final_punctuation

arg_parser = argparse.ArgumentParser(
    description=("Process the NaN-NLI Dataset for negations.")
)
arg_parser.add_argument("dataset", type=str,
                        help="the WikiFactCheck-English dataset to process")
arg_parser.add_argument("-o", "--output", type=str, default=None,
                        help="the directory where the processed data will be "
                             "written to. If not specified, defaults to "
                            f"'{DEFAULT_OUTPUT_DIR}'.")
arg_parser.add_argument("-f", "--force", action="store_true",
                        help="overwrite data in the output directory")


class WikiFactCheckEnglishDatasetProcessor(BaseDatasetProcessor):
    """WikiFactCheck-English dataset processor.

    See `README.md`.
    """

    def _process(
        self,
        dataset: str,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        with open(Path(dataset), "r") as f:
            wikifactcheck = [
                {
                    "sentence": add_final_punctuation(
                        json.loads(line).pop("claim")
                    ),
                    "negated": add_final_punctuation(
                        json.loads(line).pop("refuted", None)
                    )
                }
                for line in f
            ]
        return pd.DataFrame.from_records(
            self._clean_up_entries(wikifactcheck)
        )

    def _clean_up_entries(
        self,
        dataset: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Remove invalid entries.

        These are:

           - Entries with the "negated" field set to :obj:`None`.
           - Entries in which the "claim" and "refuted" fields have a Jaccard
             index below 0.55.
           - Entries in which the "claim" and "refuted" fields differ in length
             by 4 or more words.
           - Entries in which the field "claim" contains named entities that
             don't appear in the field "refuted" or vice versa.

        Args:
            dataset (:obj:`List[Dict[str, str]]`):
                The parsed dataset.

        Returns:
            :obj:`List[Dict[str, str]]`: The dataset dictionary with the invalid
            entries removed.
        """
        def unmatched_entities_exist(sentence: str, negated: str) -> bool:
            """Determine whether there are NE in :param:`sentence` not in :param:`negated` or vice versa.

            Args:
                sentence (:obj:`str`):
                    A sentence.
                negated (:obj:`str`):
                    The negated version of :param:`sentence`.

            Returns:
                :obj:`bool`: Whether there are NE in :param:`sentence` not in
                :param:`negated` or vice versa.
            """
            nlp = spacy.load("en_core_web_md")
            doc_sentence, doc_negated = nlp(sentence), nlp(negated)

            ents_sentence = [ent_s.text for ent_s in doc_sentence.ents]
            ents_negated = [ent_n.text for ent_n in doc_negated.ents]
            
            if len(ents_sentence) == len(ents_negated):
                s_not_in_n = any(ent_s not in ents_negated for ent_s in ents_sentence)
                n_not_in_s = any(ent_n not in ents_sentence for ent_n in ents_negated)
                return s_not_in_n or n_not_in_s
            return True

        return [e for e in tqdm(dataset)
                if e["negated"]
                and abs(len(e["sentence"].split()) - len(e["negated"].split())) <= 3
                and jaccard_similarity(e["sentence"], e["negated"]) >= 0.55
                and not unmatched_entities_exist(e["sentence"], e["negated"])]


def main(args: argparse.ArgumentParser):
    """Process WikiFactCheck-English dataset."""
    output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
    if output_dir and output_dir.exists() and not args.force:
        print(f"Output directory '{output_dir}/' already exists.")
        decision = input("Overwrite? (y/N): ")
        if decision.lower() != "y":
            sys.exit()

    wikifactcheck_processor = WikiFactCheckEnglishDatasetProcessor(
        dataset_name="WikiFactCheck-English")
    wikifactcheck_processor.process(args.dataset, output_dir=output_dir)


if __name__ == "__main__":
    main(arg_parser.parse_args())
