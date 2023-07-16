"""Base data processor.

Specific dataset processors should inherit from this base processor.
"""

import casefy
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import pandas as pd

DEFAULT_OUTPUT_DIR = "processed/"


class BaseDatasetProcessor(ABC):
    """Base dataset processor.

    Attributes:
        dataset_name (:obj:`str`):
            The name of the dataset the processor is suited for.
        default_output_dir (:obj:`pathlib.Path`):
            The default directory where the processed data will be written to.
            If not provided, defaults to "processed/".
    """

    def __init__(
        self,
        dataset_name: str,
        default_output_dir: Optional[str] = None
    ):
        self.dataset_name = dataset_name
        self.default_output_dir = (Path(default_output_dir)
                                   if default_output_dir
                                   else Path(DEFAULT_OUTPUT_DIR))

    def process(
        self,
        dataset: Any,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> None:
        """Process a dataset.

        Args:
            dataset (:obj:`Any`):
                The dataset to process.
            output_dir (:obj:`Optional[str]`):
                The directory where the processed data will be written to. If
                not specified, :attr:`default_output_dir` is used.
        """
        output_dir = Path(output_dir) if output_dir else self.default_output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"♻️  Processing dataset '{self.dataset_name}'...")
        processed_dataset = self._process(dataset, output_dir, **kwargs)
        filename = casefy.snakecase(self.dataset_name)
        processed_dataset.to_csv(output_dir/f"{filename}.tsv", sep="\t",
                                 encoding='utf-8', index=False)
        print(f"✅ Done! Output data written to '{output_dir}/'.")

    @abstractmethod
    def _process(
        self,
        dataset: Any,
        output_dir: str,
        **kwargs
    ) -> pd.DataFrame:
        """Process a dataset.

        Not meant to be called directly. To be implemented by children classes.
        """
