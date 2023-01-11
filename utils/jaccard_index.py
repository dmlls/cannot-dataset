"""Jacard index.

See `https://en.wikipedia.org/wiki/Jaccard_index`__."""

import string
from typing import Set


def jaccard_similarity(a: str, b: str) -> float:
    """Calculate the Jaccard similarity between two strings.

    Common punctuation characters are not taken into account for the
    calculation.

    Args:
        a (:obj:`str`):
            The first string.
        b (:obj:`str`):
            The second string.

    Returns:
        :obj:`float`: The Jaccard index of the two strings.
    """
    words_a: Set[str] = {w.strip(string.punctuation) for w in a.split()}
    words_b: Set[str] = {w.strip(string.punctuation) for w in b.split()}
    return len(words_a.intersection(words_b)) / len(words_a.union(words_b))
