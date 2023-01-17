"""Paraphrasis utilities."""

from typing import List
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer


class PegasusParaphraser:
    """Pre-trained Pegasus paraphraser.

    See `https://huggingface.co/tuner007/pegasus_paraphrase`__.

    Attributes:
        tokenizer (:obj:`PegasusTokenizer`):
            The Pegasus tokenizer.
        model (:obj:`PegasusForConditionalGeneration`):
            The Pegasus model.
    """

    def __init__(self):
        model_name = "tuner007/pegasus_paraphrase"
        self._torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(
        model_name).to(self._torch_device)

    def paraphrase(
        self,
        sentence: str,
        num_return_sentences: int = 1,
        num_beams: int = 4
    ) -> List[str]:
        """Paraphrase a sentence.

        Args:
            sentence (:obj:`str`):
                The sentence to paraphrase.
            num_return_sentences (:obj:`int`, `optional`, defaults to ``1``):
                The number of paraphrased versions of the sentence to return.
            num_beams (:obj:`int`, `optional`, defaults to ``4``):
                The number of beams to use for generation. See
                `https://huggingface.co/blog/how-to-generate#beam-search`__.

        Returns:
            :obj:`List[str]`: The paraphrased sentences.
        """
        batch = self.tokenizer(
            [sentence],
            truncation=True,
            padding='longest',
            max_length=60,
            return_tensors="pt"
        ).to(self._torch_device)
        paraphrased = self.model.generate(
            **batch,
            max_length=60,
            num_beams=num_beams,
            num_return_sequences=num_return_sentences,
            temperature=1.5
        )
        paraphrased_sents = self.tokenizer.batch_decode(
            paraphrased,
            skip_special_tokens=True
        )
        return paraphrased_sents


    def paraphrase_batch(
        self,
        sentences: List[str],
        num_return_sentences: int = 1,
        num_beams: int = 4
    ) -> List[List[str]]:
        """Paraphrase a batch of sentences.

        Args:
            sentences (:obj:`List[str]`):
                The sentences to paraphrase.
            num_return_sentences (:obj:`int`, `optional`, defaults to ``1``):
                The number of paraphrased versions to return per sentence.
            num_beams (:obj:`int`, `optional`, defaults to ``4``):
                The number of beams to use for generation. See
                `https://huggingface.co/blog/how-to-generate#beam-search`__.

        Returns:
            :obj:`List[List[str]]`: The paraphrased versions of each sentence,
            grouped in lists of length :param:`num_return_sentences`.
        """
        if num_return_sentences < 1:
            num_return_sentences = 1
        batch = self.tokenizer(
            sentences,
            truncation=True,
            padding='longest',
            max_length=60,
            return_tensors="pt"
        ).to(self._torch_device)
        paraphrased = self.model.generate(
            **batch,
            max_length=60,
            num_beams=num_beams,
            num_return_sequences=num_return_sentences,
            temperature=1.5
        )
        paraphrased_sents = self.tokenizer.batch_decode(
            paraphrased,
            skip_special_tokens=True
        )
        return [paraphrased_sents[i:i+num_return_sentences]
                for i in range(0, len(paraphrased_sents), num_return_sentences)]
