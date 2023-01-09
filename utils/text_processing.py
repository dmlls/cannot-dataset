"""Text processing utilities."""


def add_final_punctuation(sentence: str, character: str = ".") -> str:
    """Add a punctuation character to the end of a sentence if missing.

    Args:
        sentence (:obj:`str`):
            The sentence to add the final punctuation to, if needed.
        character (:obj:`str`, defaults to ``"."``):
            The punctuation character to add.

    Returns:
        :obj:`str`: The sentence ending with the specified punctuation.
    """
    if not sentence:
        return ""
    return f"{sentence}{character}" if sentence[-1] != character else sentence
