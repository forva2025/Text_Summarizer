# Text Summarizer

[![Tests](https://github.com/forva2025/Text_Summarizer/actions/workflows/tests.yml/badge.svg)](https://github.com/forva2025/Text_Summarizer/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![NLTK](https://img.shields.io/badge/NLTK-3.9.2-154f3c)](https://www.nltk.org/)
[![Pytest](https://img.shields.io/badge/tested_with-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-000000.svg)](https://peps.python.org/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A local, frequency-based extractive text summarizer with a polished Streamlit interface. It ranks sentences using meaningful word frequency and returns the strongest sentences in their original order. No external AI API or API key is required.

## Features

- Extractive English text summarization using NLTK
- Adjustable summary length from 1 to 10 sentences
- Original-order output for better readability
- Word-count, sentence-count, and reduction metrics
- Built-in example, clear action, and summary download
- Input validation and helpful UI error messages
- Cached, on-demand NLTK resource setup
- Offline and deterministic automated unit tests
- GitHub Actions test matrix for Python 3.10–3.13

## How the algorithm works

1. Split the source into sentences and lowercase word tokens.
2. Remove punctuation, non-alphabetic tokens, and common English stop words.
3. Count each remaining word's frequency in the document.
4. Score each sentence by adding the frequencies of its meaningful words.
5. Select the requested number of highest-scoring sentences.
6. Restore the selected sentences to their original document order.

This is an **extractive** summarizer: it selects complete source sentences rather than generating new wording. It is fast and transparent, but it does not understand meaning as deeply as a large language model.

## Project structure

```text
Text_Summarizer/
├── .github/workflows/tests.yml  # Continuous-integration test workflow
├── tests/test_summary.py        # Unit tests for the summarization engine
├── app.py                       # Streamlit user interface
├── summary.py                   # Reusable summarization logic
├── requirements.txt             # Runtime dependencies
├── requirements-dev.txt         # Runtime and test dependencies
├── LICENSE                      # MIT license
└── README.md                    # Project documentation
```

## Quick start

### 1. Clone and enter the project

```bash
git clone https://github.com/forva2025/Text_Summarizer.git
cd Text_Summarizer
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the app

```bash
python -m streamlit run app.py
```

Streamlit will print the local app address, normally `http://localhost:8501`.

On the first run, the app downloads NLTK's `punkt`, `punkt_tab`, and `stopwords` datasets. Later runs reuse the local copies.

## Use the summarizer from Python

```python
from summary import ensure_nltk_resources, summarize_text

ensure_nltk_resources()

text = """Your longer English passage goes here. Add several sentences so the
frequency scorer has enough context. The function returns an extractive summary."""

result = summarize_text(text, num_sentences=2)
print(result)
```

## Run the tests

Install the development dependencies and run pytest:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The unit tests mock the language tokenizers and stop-word corpus, so they do not need network access or downloaded NLTK data. Pushes and pull requests are also tested automatically by GitHub Actions.

## The original `TypeError`, explained

The failing condition was:

```python
if word in word_tokenize:
```

`word_tokenize` is a **function**. The `in` operator requires an iterable value such as a dictionary, list, or set, so Python raised `TypeError: argument of type 'function' is not iterable`. The intended lookup is against the frequency dictionary:

```python
if word in word_frequencies:
```

The corrected implementation uses that dictionary for both membership and scoring. The former line 45 only appeared in the traceback because it called `summarize_text`; the underlying defect was inside the function at former line 38.

## Configuration and limits

- The UI accepts up to 50,000 characters per run.
- The sidebar permits summaries of 1–10 sentences.
- English input is recommended because the included stop-word corpus is English.
- If the requested summary is longer than the source, all source sentences are returned.
- Text is processed in the local Streamlit process and is not sent to an external model.

## Troubleshooting

### NLTK resource error

Confirm that the computer has internet access for the first app run. To install the resources manually:

```bash
python -m nltk.downloader punkt punkt_tab stopwords
```

### `streamlit` is not recognized

Activate the project's virtual environment and use the module form:

```bash
python -m streamlit run app.py
```

### PowerShell blocks virtual-environment activation

Run Python directly from `.venv\Scripts\python.exe` or review PowerShell's execution-policy documentation before changing your local policy.

## Contributing

1. Fork the repository and create a focused branch.
2. Add or update tests for behavior changes.
3. Run `python -m pytest -q` locally.
4. Open a pull request describing the change and its motivation.

## License

Distributed under the [MIT License](LICENSE).
