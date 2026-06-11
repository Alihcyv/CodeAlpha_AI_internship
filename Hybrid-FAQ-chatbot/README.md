# 🤖 m10 Hybrid FAQ Bot

[Click here to test the application in your browser](https://codealphaaiinternship-nefezpy2pzzydug78qtrnd.streamlit.app)
## Project Overview
This project implements a **Hybrid Search Architecture** to combine the strengths of semantic meaning and exact keyword matching, ensuring accurate and hallucination-free responses.

## Features
- **Hybrid Search Engine**: Combines **SBERT (Dense Retrieval)** and **BM25 (Sparse Retrieval)**.
- **RRF Ranking**: Uses **Reciprocal Rank Fusion (RRF)** to merge results from both search methods.
- **Hallucination Guardrails**: Implements a **Cosine Similarity Threshold** to prevent the bot from guessing when it doesn't know the answer.
- **Modern UI**: Built with **Streamlit** for a seamless.
- **Optimized Performance**: Resource caching using `@st.cache_resource` for near-instant model loading.

## Engineering Decisions & Optimizations
- **Hybrid Search Architecture (Dense + Sparse)**:
I decided against using only vector embeddings because they can sometimes miss exact keywords (e.g., specific product IDs or technical terms). By adding BM25, the bot can handle both semantic queries ("How do I get my money back?") and keyword-specific queries ("m10-ID requirements") with equal precision.
- **Reciprocal Rank Fusion (RRF)**:
Since Vector scores (0 to 1) and BM25 scores (0 to ∞) operate on different scales, they cannot be simply added. I implemented RRF, which ignores the raw scores and focuses on the rank of the documents. This ensures a fair and balanced merge of the two search results.
- **Cosine Similarity Guardrail**:
To eliminate AI hallucinations, I implemented a final validation step. Even if a document is the "best match" in the list, the bot calculates the actual Cosine Similarity. If the score is below 0.6, the bot triggers a fallback response ("I don't have enough information...") instead of giving a wrong answer.
- **Resource Caching (@st.cache_resource)**:
Loading a Sentence-Transformer model into RAM takes several seconds. To prevent the app from reloading the model on every user interaction, I used Streamlit's resource caching. This ensures the model is loaded into memory only once, making responses near-instant.

##  Tech Stack
- **Language**: Python 3.10+
- **NLP Models**: `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Search Algorithms**: BM25s, Cosine Similarity, RRF
- **Frontend**: Streamlit
- **Data Handling**: NumPy
- **Deployment**: Streamlit Cloud


