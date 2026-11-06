# Mini Search Engine (Information Retrieval System)

Course Assignment Submission

Course: Web Search and Mining 
Project: Implementation of a Modular Text Search Engine
Live Deployed Application: https://mini-search-engine-app-assignment.streamlit.app

Submitted By:
Nikita Bardan Lugun (Roll No: B124078),
Jyotismita Das (Roll No: B124057)

A modular, lightweight Information Retrieval (IR) search engine built in Python 3 with a Streamlit GUI. This project demonstrates the core architectural components of a text search engine—from raw document loading, tokenization, and normalization to inverted index construction, boolean query parsing, and wildcard matching—without relying on high-level external search libraries (such as Elasticsearch, Solr, Lucene, or Whoosh).


---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```
*(Or `cd mini_search_engine; streamlit run app.py`)*

### 3. Run Unit Tests
```bash
pytest mini_search_engine/tests
```
or
```bash
cd mini_search_engine
pytest
```

---

## Required Project Structure

```text
mini_search_engine/
│
├── app.py                      # Streamlit frontend web application
├── requirements.txt            # Minimal dependencies (streamlit, pytest)
├── README.md                   # Comprehensive documentation and guide
│
├── data/
│   └── documents/              # Sample plain-text document corpus
│       ├── doc1.txt            # Artificial Intelligence
│       ├── doc2.txt            # Machine Learning
│       ├── doc3.txt            # Database Systems
│       ├── doc4.txt            # Computer Networks
│       ├── doc5.txt            # Operating Systems
│       ├── doc6.txt            # Information Retrieval
│       ├── doc7.txt            # Search Engines
│       └── doc8.txt            # Programming in Python
│
├── src/                        # Core Information Retrieval modules
│   ├── __init__.py             # Package exports
│   ├── document_loader.py      # Component 1: File loading & validation
│   ├── tokenizer.py            # Component 2: Lexical token extraction
│   ├── normalizer.py           # Component 3: Case folding & token cleanup
│   ├── inverted_index.py       # Component 4: Inverted index construction
│   ├── query_processor.py      # Component 5: Boolean AND / OR query engine
│   └── wildcard_processor.py   # Component 6: Vocabulary wildcard matcher
│
└── tests/                      # Unit test suite
    ├── __init__.py
    ├── test_document_loader.py
    ├── test_tokenizer.py
    ├── test_normalizer.py
    ├── test_inverted_index.py
    ├── test_query_processor.py
    └── test_wildcard_processor.py
```

For full theory explanations, detailed module designs, set operations, and wildcard matching architecture, see [mini_search_engine/README.md](file:///c:/Users/DELL/Downloads/WSM%20assignment/mini_search_engine/README.md).
