"""Post length the way X counts it."""

import re


def x_length(text):
    """Weighted length: any URL counts 23, most Latin characters 1, emoji and CJK 2."""
    text = re.sub(r"https?://\S+", "x" * 23, text)
    n = 0
    for ch in text:
        cp = ord(ch)
        light = (cp <= 4351 or 8192 <= cp <= 8205 or 8208 <= cp <= 8223
                 or 8242 <= cp <= 8247)
        n += 1 if light else 2
    return n
