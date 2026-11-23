"""Tests for the summarization engine."""

import pytest

import summary


@pytest.fixture(autouse=True)
def fake_nltk_language_tools(monkeypatch):
    """Keep tests deterministic and independent of downloaded NLTK data."""

    def split_sentences(text):
        return [part.strip() + "." for part in text.split(".") if part.strip()]

    def split_words(text):
        return text.replace(".", "").replace(",", "").split()

    monkeypatch.setattr(summary, "sent_tokenize", split_sentences)
    monkeypatch.setattr(summary, "word_tokenize", split_words)
    monkeypatch.setattr(summary.stopwords, "words", lambda _language: ["the", "is"])


def test_selects_the_highest_scoring_sentence():
    text = "Cats sleep quietly. Dogs run quickly. Cats chase cats."
    assert summary.summarize_text(text, 1) == "Cats chase cats."


def test_selected_sentences_keep_original_order():
    text = "Alpha alpha appears. Bridge sentence. Beta beta beta appears."
    assert summary.summarize_text(text, 2) == (
        "Alpha alpha appears. Beta beta beta appears."
    )


def test_request_larger_than_document_returns_all_sentences():
    assert summary.summarize_text("First item. Second item.", 10) == (
        "First item. Second item."
    )


@pytest.mark.parametrize("value", ["", "   ", "\n"])
def test_empty_text_returns_empty_string(value):
    assert summary.summarize_text(value) == ""


@pytest.mark.parametrize("value", [0, -1])
def test_sentence_count_must_be_positive(value):
    with pytest.raises(ValueError, match="at least 1"):
        summary.summarize_text("Valid text.", value)


@pytest.mark.parametrize("value", [1.5, "2", True])
def test_sentence_count_must_be_an_integer(value):
    with pytest.raises(TypeError, match="must be an integer"):
        summary.summarize_text("Valid text.", value)


def test_text_must_be_a_string():
    with pytest.raises(TypeError, match="must be a string"):
        summary.summarize_text(None)


def test_only_stop_words_are_returned_unchanged():
    assert summary.summarize_text("The is the.") == "The is the."
