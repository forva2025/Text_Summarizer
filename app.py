"""Streamlit interface for the frequency-based text summarizer."""

from __future__ import annotations

import html

import streamlit as st
from nltk.tokenize import sent_tokenize

from summary import ensure_nltk_resources, summarize_text

SAMPLE_TEXT = """Artificial intelligence allows computer systems to perform tasks that usually require human intelligence. These tasks include learning, reasoning, perception, and language understanding.

Machine learning is a branch of artificial intelligence in which algorithms discover patterns in data. Instead of following only hand-written rules, a trained model can generalize from examples and make predictions about new information.

Deep learning is a machine learning approach based on neural networks with many layers. It has driven major advances in computer vision, speech recognition, and natural language processing, although it can require substantial data and computing power."""

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {max-width: 1120px; padding-top: 2.5rem;}
      [data-testid="stMetric"] {
        background: rgba(127, 127, 127, 0.08);
        border: 1px solid rgba(127, 127, 127, 0.18);
        border-radius: 0.75rem;
        padding: 0.8rem 1rem;
      }
      .app-subtitle {color: #6b7280; font-size: 1.05rem; margin-top: -0.6rem;}
      .summary-card {
        border-left: 4px solid #7c3aed;
        background: rgba(124, 58, 237, 0.08);
        border-radius: 0.4rem;
        padding: 1rem 1.2rem;
        line-height: 1.7;
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def prepare_nltk() -> None:
    """Install required tokenizer data once per Streamlit process."""

    ensure_nltk_resources()


def word_count(value: str) -> int:
    """Count whitespace-delimited words for display metrics."""

    return len(value.split())


try:
    prepare_nltk()
except RuntimeError as error:
    st.error(f"The language resources could not be initialized: {error}")
    st.info("Check your internet connection, then restart the app.")
    st.stop()

with st.sidebar:
    st.header("Summary settings")
    sentence_count = st.slider(
        "Maximum summary sentences",
        min_value=1,
        max_value=10,
        value=3,
        help="If the source is shorter, every available sentence is returned.",
    )
    st.divider()
    st.subheader("How it works")
    st.caption(
        "The app removes common English stop words, scores the remaining words "
        "by frequency, and extracts the strongest sentences in their original order."
    )
    st.info("Your text is processed locally and is not sent to an AI service.")

st.title("📝 Text Summarizer")
st.markdown(
    '<p class="app-subtitle">Turn long English text into a concise, extractive summary.</p>',
    unsafe_allow_html=True,
)

if "source_text" not in st.session_state:
    st.session_state.source_text = ""

load_col, clear_col, _ = st.columns([1, 1, 4])
with load_col:
    if st.button("Load example", use_container_width=True):
        st.session_state.source_text = SAMPLE_TEXT
        st.rerun()
with clear_col:
    if st.button("Clear", use_container_width=True):
        st.session_state.source_text = ""
        st.rerun()

with st.form("summarizer_form"):
    source_text = st.text_area(
        "Text to summarize",
        key="source_text",
        height=300,
        max_chars=50_000,
        placeholder="Paste an article, report, or passage here…",
        help="English text works best. Maximum length: 50,000 characters.",
    )
    submitted = st.form_submit_button(
        "Summarize text", type="primary", use_container_width=True
    )

if submitted:
    if not source_text.strip():
        st.warning("Enter some text before creating a summary.")
    else:
        try:
            with st.spinner("Finding the most informative sentences…"):
                result = summarize_text(source_text, sentence_count)

            source_words = word_count(source_text)
            summary_words = word_count(result)
            reduction = (
                round((1 - summary_words / source_words) * 100) if source_words else 0
            )
            source_sentences = len(sent_tokenize(source_text.strip()))

            st.subheader("Summary")
            st.markdown(
                f'<div class="summary-card">{html.escape(result)}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "Download summary",
                data=result,
                file_name="summary.txt",
                mime="text/plain",
            )

            metric_one, metric_two, metric_three, metric_four = st.columns(4)
            metric_one.metric("Original words", f"{source_words:,}")
            metric_two.metric("Summary words", f"{summary_words:,}")
            metric_three.metric("Reduction", f"{reduction}%")
            metric_four.metric("Source sentences", source_sentences)
        except (LookupError, TypeError, ValueError) as error:
            st.error(f"The text could not be summarized: {error}")

st.divider()
st.caption("Frequency-based extractive summarization · Built with Streamlit and NLTK")
