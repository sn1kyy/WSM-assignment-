"""
Mini Search Engine - Streamlit Frontend GUI
Demonstrates Information Retrieval pipeline:
Document Loading -> Tokenization -> Normalization -> Inverted Index -> Query & Wildcard Processing
"""

import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import streamlit as st

# Ensure project root is on sys.path so 'src' imports resolve cleanly
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.document_loader import DocumentLoader
from src.inverted_index import InvertedIndex
from src.normalizer import Normalizer
from src.query_processor import QueryProcessor
from src.tokenizer import Tokenizer
from src.wildcard_processor import WildcardProcessor

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


# -----------------------------------------------------------------------------
# Caching: Load documents & build Inverted Index once at startup
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=True)
def initialize_search_engine(docs_dir: Path) -> Tuple[Dict[str, str], InvertedIndex, QueryProcessor, WildcardProcessor]:
    """
    Load all documents, construct the inverted index, and initialize processors.
    Cached with @st.cache_resource so the index is built once and persists across searches.
    """
    loader = DocumentLoader(docs_dir)
    documents = loader.load_documents()

    tokenizer = Tokenizer()
    normalizer = Normalizer()

    index = InvertedIndex(tokenizer=tokenizer, normalizer=normalizer)
    index.build(documents)

    query_processor = QueryProcessor(index, normalizer=normalizer)
    wildcard_processor = WildcardProcessor(index, normalizer=normalizer)

    return documents, index, query_processor, wildcard_processor


def generate_snippet(text: str, query_terms: List[str], max_len: int = 180) -> str:
    """
    Generate a relevant short snippet from the document text around matching query terms.
    """
    if not text:
        return "*(Empty document)*"

    lower_text = text.lower()
    match_pos = -1

    # Find the earliest occurrence of any query term
    for term in query_terms:
        clean = term.strip(" *").lower()
        if clean:
            pos = lower_text.find(clean)
            if pos != -1 and (match_pos == -1 or pos < match_pos):
                match_pos = pos

    if match_pos == -1:
        # Fall back to opening sentence
        snippet = text[:max_len].strip()
        return snippet + "..." if len(text) > max_len else snippet

    # Center snippet window around match
    start = max(0, match_pos - 40)
    end = min(len(text), match_pos + max_len)
    prefix = "..." if start > 0 else ""
    suffix = "..." if end < len(text) else ""
    return prefix + text[start:end].strip() + suffix


# -----------------------------------------------------------------------------
# Streamlit UI
# -----------------------------------------------------------------------------
def main() -> None:
    st.set_page_config(
        page_title="Mini Search Engine",
        page_icon="🔍",
        layout="wide",
    )

    # 1. Application Title
    st.title("🔍 Mini Search Engine")
    st.caption("Information Retrieval System — Tokenization, Case-Folding, Inverted Index & Wildcard Processing")

    # Initialize IR system
    documents, index, query_processor, wildcard_processor = initialize_search_engine(DOCUMENTS_DIR)

    # Sidebar: Index Statistics & Quick Guide
    with st.sidebar:
        st.header("📊 Index Statistics")
        st.metric("Total Documents", len(documents))
        st.metric("Vocabulary Terms", index.total_terms)

        st.markdown("---")
        st.subheader("💡 Example Queries")
        st.markdown(
            """
            - **Normal Term:** `computer`, `database`, `search`
            - **AND Query:** `machine AND learning`
            - **OR Query:** `database OR network`
            - **Prefix Wildcard:** `app*`
            - **Suffix Wildcard:** `*tion`
            - **Infix Wildcard:** `*app*`, `comp*ter`
            """
        )

        st.markdown("---")
        with st.expander("📚 View Document Collection"):
            for doc_name in sorted(documents.keys()):
                st.write(f"- `{doc_name}`")

        with st.expander("🔤 Vocabulary Sample"):
            vocab_sample = sorted(list(index.get_vocabulary()))[:40]
            st.write(", ".join(vocab_sample) + ("..." if len(index.get_vocabulary()) > 40 else ""))

    # 2. Search Input Box
    query = st.text_input(
        "Enter search query (Supports single terms, AND / OR, and * wildcards):",
        placeholder="e.g. machine AND learning, app*, *tion, database OR network",
        key="search_input",
    )

    # 3. Search Button
    search_clicked = st.button("Search", type="primary")

    st.markdown("---")
    st.subheader("Results")

    # 4. Search Execution & Read-Only Results Area
    if search_clicked or query:
        query_str = query.strip()
        if not query_str:
            st.info("Please enter a query in the search box above.")
            return

        is_wildcard = WildcardProcessor.is_wildcard_query(query_str)

        matched_terms: List[str] = []
        result_doc_ids: Set[str] = set()

        if is_wildcard:
            # Wildcard Pipeline: match terms against vocabulary, then fetch postings
            st.info(f"🔎 **Query Type:** Wildcard Query (`{query_str}`)")
            matched_terms = wildcard_processor.match_terms(query_str)

            if matched_terms:
                st.markdown(
                    f"**Matched Vocabulary Terms ({len(matched_terms)}):** "
                    + ", ".join([f"`{t}`" for t in matched_terms])
                )
                result_doc_ids = wildcard_processor.search(query_str)
            else:
                st.warning(f"No vocabulary terms matched the wildcard pattern `{query_str}`.")
                return
        else:
            # Normal Query Pipeline: single-term, AND, or OR queries
            st.info(f"🔎 **Query Type:** Normal / Boolean Query (`{query_str}`)")
            result_doc_ids = query_processor.process_query(query_str)
            matched_terms = query_str.split()

        # Display Result Count & Matches
        if not result_doc_ids:
            st.warning(f"No matching documents found for query: `{query_str}`.")
        else:
            st.success(f"Found **{len(result_doc_ids)}** matching document(s).")

            # Sort document IDs for deterministic presentation
            sorted_docs = sorted(list(result_doc_ids))

            for idx, doc_id in enumerate(sorted_docs, start=1):
                doc_text = documents.get(doc_id, "")
                snippet = generate_snippet(doc_text, matched_terms)

                with st.container():
                    st.markdown(f"### {idx}. 📄 `{doc_id}`")
                    st.markdown(f"> {snippet}")
                    with st.expander(f"View full text of `{doc_id}`"):
                        st.text(doc_text)
                    st.divider()


if __name__ == "__main__":
    main()
