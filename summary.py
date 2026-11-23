"""Frequency-based extractive text summarization utilities."""

from __future__ import annotations

from collections import Counter
from numbers import Integral

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

NLTK_RESOURCES = {
    "tokenizers/punkt": "punkt",
    "tokenizers/punkt_tab": "punkt_tab",
    "corpora/stopwords": "stopwords",
}


def ensure_nltk_resources() -> None:
    """Download only the NLTK data packages that are not already installed."""

    for resource_path, package_name in NLTK_RESOURCES.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            if not nltk.download(package_name, quiet=True):
                raise RuntimeError(
                    f"Could not download the required NLTK resource: {package_name}."
                )


def summarize_text(text: str, num_sentences: int = 2) -> str:
    """Return the highest-scoring sentences in their original document order.

    Words are scored by frequency after English stop words and non-alphabetic
    tokens are removed. Call :func:`ensure_nltk_resources` once before use.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(num_sentences, bool) or not isinstance(num_sentences, Integral):
        raise TypeError("num_sentences must be an integer")
    if num_sentences < 1:
        raise ValueError("num_sentences must be at least 1")

    cleaned_text = text.strip()
    if not cleaned_text:
        return ""

    sentences = sent_tokenize(cleaned_text)
    words = word_tokenize(cleaned_text.lower())
    stop_words = set(stopwords.words("english"))
    word_frequencies = Counter(
        word for word in words if word.isalpha() and word not in stop_words
    )

    if not sentences or not word_frequencies:
        return cleaned_text

    sentence_scores: list[tuple[int, int]] = []
    for index, sentence in enumerate(sentences):
        score = sum(
            word_frequencies[word]
            for word in word_tokenize(sentence.lower())
            if word in word_frequencies
        )
        sentence_scores.append((index, score))

    summary_size = min(num_sentences, len(sentences))
    highest_scoring = sorted(
        sentence_scores, key=lambda item: (-item[1], item[0])
    )[:summary_size]
    selected_indices = sorted(index for index, _ in highest_scoring)
    return " ".join(sentences[index] for index in selected_indices)


if __name__ == "__main__":
    example_text = (
        "Artificial intelligence enables machines to perform tasks associated "
        "with human intelligence. Machine learning systems can improve from data "
        "without being explicitly programmed. Deep learning uses multilayer neural "
        "networks to learn patterns from large amounts of data."
    )
    ensure_nltk_resources()
    print(summarize_text(example_text, num_sentences=2))
