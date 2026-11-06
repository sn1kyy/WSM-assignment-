# Mini Search Engine (Information Retrieval System)

A modular, lightweight Information Retrieval (IR) search engine built in Python 3 with a Streamlit GUI. This project demonstrates the core architectural components of a text search engine—from raw document loading, tokenization, and normalization to inverted index construction, boolean query parsing, and wildcard matching—without relying on high-level external search libraries (such as Elasticsearch, Solr, Lucene, or Whoosh).

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objective](#2-objective)
3. [Architecture & Pipeline](#3-architecture--pipeline)
4. [Folder Structure](#4-folder-structure)
5. [Explanation of Each Module](#5-explanation-of-each-module)
6. [What Tokenization Is](#6-what-tokenization-is)
7. [What Normalization / Case Folding Is](#7-what-normalization--case-folding-is)
8. [What an Inverted Index Is](#8-what-an-inverted-index-is)
9. [How Query Processing Works](#9-how-query-processing-works)
10. [How AND / OR Queries Work](#10-how-and--or-queries-work)
11. [How Wildcard Searching Works](#11-how-wildcard-searching-works)
12. [How the Streamlit GUI Works](#12-how-the-streamlit-gui-works)
13. [Installation Instructions](#13-installation-instructions)
14. [How to Run the Application](#14-how-to-run-the-application)
15. [How to Run Tests](#15-how-to-run-tests)
16. [Example Queries and Expected Behavior](#16-example-queries-and-expected-behavior)
17. [Limitations](#17-limitations)
18. [Possible Future Improvements](#18-possible-future-improvements)

---

## 1. Project Overview

Search engines are foundational to information retrieval. Rather than inspecting the full text of every document for every search request, modern search engines preprocess documents offline into a structured inverted index. When a user submits a query, the search engine resolves terms rapidly through set operations on precomputed postings lists.

This project implements this complete, end-to-end pipeline in clean, modular Python 3 standard library code, providing an intuitive, interactive web interface powered by Streamlit.

---

## 2. Objective

- Demonstrate fundamental Information Retrieval and Search Engine principles clearly and hands-on.
- Provide a clean, strictly decoupled modular architecture where each component has a single, well-defined responsibility.
- Implement tokenization, normalization, inverted index construction, boolean query evaluation (AND, OR), and wildcard searches from scratch.
- Provide unit tests verifying each component independently.
- Present a clean, beginner-friendly Streamlit web interface with read-only result presentation, match snippets, and collection analytics.

---

## 3. Architecture & Pipeline

```text
       Raw Document Files (.txt)
                   │
                   ▼
         [ 1. Document Loader ]
                   │ Mapping {doc_id: raw_text}
                   ▼
           [ 2. Tokenizer ]
                   │ Word tokens preserving casing
                   ▼
           [ 3. Normalizer ]
                   │ Lowercase, punctuation-trimmed tokens
                   ▼
        [ 4. Inverted Index ]
        (term -> {doc_id, ...})
                   ▲
                   │
         User Query via Web UI
                   │
                   ▼
       Is '*' present in query?
         ├── YES ──► [ 6. Wildcard Processor ]
         │                 │
         │                 ├─ Match pattern against vocabulary (O(V))
         │                 └─ Retrieve & Union postings lists
         │
         └── NO  ──► [ 5. Query Processor ]
                           │
                           ├─ Normalize query terms
                           └─ Evaluate Single, AND (∩), OR (∪)
                                   │
                                   ▼
                   [ 7. Streamlit Frontend GUI ]
                   - Read-only matching document list
                   - Document count & keyword snippets
                   - Query classification badge
```

---

## 4. Folder Structure

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

---

## 5. Explanation of Each Module

| Module | Responsibility | Key Classes & Methods |
| :--- | :--- | :--- |
| `src/document_loader.py` | Scans the document directory, reads `.txt` files into memory, handles missing directories and empty files gracefully. Does not perform NLP preprocessing. | `DocumentLoader.load_documents()` |
| `src/tokenizer.py` | Extracts individual lexical tokens (words) using regex word boundaries `\b\w+\b`. Discards whitespace and punctuation while strictly preserving original casing. | `Tokenizer.tokenize(text)` |
| `src/normalizer.py` | Standardizes tokens into canonical form via case folding (lowercase) and trimming residual punctuation. | `Normalizer.normalize_token(token)`, `normalize_tokens(tokens)` |
| `src/inverted_index.py` | Preprocesses documents using tokenizer and normalizer to build the core index mapping `term -> Set[doc_id]`. Provides vocabulary access and $O(1)$ term postings lookup. | `InvertedIndex.build()`, `search_term()`, `get_vocabulary()` |
| `src/query_processor.py` | Parses user queries, handles single-term searches, boolean `AND` (set intersection), and boolean `OR` (set union), ensuring terms undergo identical normalization. | `QueryProcessor.process_query(query)` |
| `src/wildcard_processor.py` | Translates user wildcard patterns (`*`) into safe regex, matches them against the index vocabulary ($O(V)$), and unions postings lists without re-scanning documents. | `WildcardProcessor.match_terms()`, `search()` |
| `app.py` | Interactive Streamlit GUI. Caches the index at startup with `@st.cache_resource`, accepts input, executes pipeline, and presents read-only results with contextual snippets. | `main()`, `initialize_search_engine()` |

---

## 6. What Tokenization Is

**Tokenization** is the first stage in textual information retrieval. It converts an unstructured continuous stream of characters into discrete meaningful semantic units called **tokens** (typically words).

- In our system, `Tokenizer` identifies word boundaries using regular expressions, stripping punctuation characters (periods, commas, semicolons, brackets) and extraneous whitespace.
- Crucially, tokenization is kept strictly decoupled from normalization: casing is preserved at this stage (e.g., `"Apple is a fruit."` $\rightarrow$ `["Apple", "is", "a", "fruit"]`).

---

## 7. What Normalization / Case Folding Is

**Normalization** is the process of mapping linguistic surface variations of a word into a single canonical form so that query terms match document terms regardless of casing or formatting.

- **Case Folding:** Converts characters to lowercase (e.g., `Apple`, `APPLE`, and `ApPlE` all map to `apple`). In modern English retrieval, lowercasing provides substantial improvements in recall without significant precision penalty.
- **Punctuation Trimming:** Cleans any residual edge punctuation from tokens (e.g., `'database'` $\rightarrow$ `database`).

---

## 8. What an Inverted Index Is

An **Inverted Index** is the primary data structure of information retrieval. Traditional databases organize data by document (forward index: document $\rightarrow$ list of words). An inverted index flips this relationship:

$$\text{Term} \longrightarrow \{\text{Doc ID}_1, \text{Doc ID}_2, \dots\}$$

### Conceptual Example:
- **doc1:** `"apple banana"`
- **doc2:** `"apple computer"`

The resulting Inverted Index:
```json
{
  "apple": ["doc1", "doc2"],
  "banana": ["doc1"],
  "computer": ["doc2"]
}
```

### Why It Matters:
To find which documents contain `"apple"`, the search engine does not read any document files at runtime. It performs an immediate $O(1)$ dictionary lookup and retrieves the postings set `{"doc1", "doc2"}`.

---

## 9. How Query Processing Works

When a user submits a query:
1. The engine checks if the query contains a wildcard (`*`).
2. If not, the `QueryProcessor` parses the query string:
   - Cleans dangling operators.
   - Detects boolean operators (`OR`, `AND`) in a case-insensitive manner.
   - Normalizes terms using the same `Normalizer` used during indexing.
   - Retrieves postings for each term from the inverted index.
   - Applies set algebra to calculate the final document set.

---

## 10. How AND / OR Queries Work

Boolean retrieval applies mathematical set theory to postings lists:

### AND Query (Intersection $\cap$)
- Query: `machine AND learning`
- Let $P(\text{machine}) = \{\text{doc1}, \text{doc2}, \text{doc4}\}$
- Let $P(\text{learning}) = \{\text{doc1}, \text{doc2}\}$
- Result: $P(\text{machine}) \cap P(\text{learning}) = \{\text{doc1}, \text{doc2}\}$
- Documents must contain **all** specified terms.

### OR Query (Union $\cup$)
- Query: `database OR network`
- Let $P(\text{database}) = \{\text{doc3}\}$
- Let $P(\text{network}) = \{\text{doc2}, \text{doc4}\}$
- Result: $P(\text{database}) \cup P(\text{network}) = \{\text{doc2}, \text{doc3}, \text{doc4}\}$
- Documents containing **any** of the specified terms are returned.

---

## 11. How Wildcard Searching Works

A naive wildcard implementation would scan every document for string patterns—a prohibitive $O(N \times L)$ operation.

Our `WildcardProcessor` operates on the **vocabulary** of the inverted index ($O(V)$):
1. **Pattern Normalization & Safe Regex Translation:**
   - Converts user pattern to lowercase: `App*` $\rightarrow$ `app*`.
   - Splits on `*` and safely escapes literals via `re.escape()` to prevent regex injection attacks.
   - Joins parts with `.*` anchored by `^` and `$`: `app*` $\rightarrow$ `^app.*$`.
2. **Vocabulary Matching:**
   - Evaluates the compiled regex against `index.get_vocabulary()`.
   - Example: For `app*`, matches `['apple', 'application', 'applied']`.
3. **Postings Retrieval & Merge:**
   - Retrieves the precomputed postings list for each matched vocabulary term.
   - Computes the union $\bigcup_{t \in \text{matches}} P(t)$ to obtain the final document set.

> **Extensibility Note:** The architecture allows substituting or augmenting regex matching with more advanced data structures (such as a Permuterm Index or $k$-gram index) without redesigning `app.py` or `inverted_index.py`.

---

## 12. How the Streamlit GUI Works

`app.py` delivers a clean web application:
- **Startup Indexing & Caching (`@st.cache_resource`):** Loads the documents and builds the inverted index once when the app launches. Subsequent searches do not rebuild the index.
- **Search Bar & Controls:** Simple `st.text_input` and `st.button("Search")`.
- **Query Classification:** Displays a visual alert indicating whether the query was executed as a Normal Boolean Query or a Wildcard Query.
- **Read-Only Result Cards:** Shows total match count, filenames, generated textual excerpts/snippets, and an expandable viewer for the full document text.
- **Sidebar Analytics:** Displays document count, vocabulary size, example queries, and vocabulary terms.

---

## 13. Installation Instructions

### Prerequisites
- Python 3.9 or higher (tested on Python 3.13)
- pip package manager

### Steps
1. Open a terminal / command prompt.
2. Navigate to the project directory:
   ```bash
   cd mini_search_engine
   ```
3. Install the minimal dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 14. How to Run the Application

Launch the Streamlit web server:

```bash
streamlit run app.py
```

The browser will open automatically at `http://localhost:8501`.

---

## 15. How to Run Tests

The project includes unit tests for all modules.

### Using Pytest:
```bash
pytest
```
Or with verbose output:
```bash
pytest -v
```

### Using Standard Library Unittest:
```bash
python -m unittest discover tests
```

---

## 16. Example Queries and Expected Behavior

| Query | Query Type | Matched Documents | Explanation |
| :--- | :--- | :--- | :--- |
| `computer` | Single Term | `doc1.txt`, `doc2.txt`, `doc4.txt`, `doc5.txt` | Documents mentioning "computer". |
| `machine AND learning` | Boolean AND | `doc1.txt`, `doc2.txt` | Documents containing both words. |
| `database OR network` | Boolean OR | `doc3.txt`, `doc4.txt` | Documents containing either database or network. |
| `app*` | Wildcard Prefix | `doc1.txt`, `doc2.txt`, `doc5.txt`, `doc7.txt`, `doc8.txt` | Matches vocabulary terms: `apple`, `application`. |
| `*tion` | Wildcard Suffix | Multiple documents | Matches vocabulary terms: `application`, `classification`, `communication`, `construction`, `information`, `intention`, `navigation`, `optimization`, `prediction`, `recommendation`, `satisfaction`, `tokenization`, `transaction`, `transmission`. |
| `comp*ter` | Wildcard Infix | `doc1.txt`, `doc2.txt`, `doc4.txt`, `doc5.txt` | Matches vocabulary term: `computer`. |
| `quantum` | Unknown Term | *(None)* | Returns informative message: "No matching documents found". |

---

## 17. Limitations

- **Exact String Matching (No Stemming/Lemmatization):** Plural forms like `computers` and singular `computer` are treated as separate vocabulary terms (unless wildcarded with `computer*`).
- **Unranked Boolean Retrieval:** Results are returned as binary matching sets without term frequency (TF-IDF) or BM25 relevance score ranking.
- **In-Memory Scale:** The inverted index is maintained in memory; suitable for small-to-medium collections rather than billions of web pages.

---

## 18. Possible Future Improvements

1. **Stemming / Lemmatization:** Integrate Porter Stemmer or Snowball Stemmer to conflate morphological variants (e.g. `retrieve`, `retrieval`, `retrieving`).
2. **Ranked Retrieval (TF-IDF / BM25):** Compute term frequency and inverse document frequency weights to sort results by relevance score.
3. **Positional / Phrase Indexing:** Store word offsets in postings to enable exact phrase queries such as `"machine learning"`.
4. **Permuterm / $k$-gram Index:** Accelerate wildcard search from $O(V)$ vocabulary scans to $O(1)$ tree/hash lookups.
5. **Spelling Correction:** Use Levenshtein distance or $k$-gram overlap to suggest "Did you mean...?" for queries with typos.
