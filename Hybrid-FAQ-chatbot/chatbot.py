import bm25s
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

TOP_K_CANDIDATES = 3 
RRF_K = 60           
SIMILARITY_THRESHOLD = 0.6 

faq_data = {
    # Security & Trust
    "Are my funds safe and secure in m10?": 
        "Yes, m10 ensures the safety of your funds. Our team works tirelessly to implement all necessary security measures to keep your money protected.",
    
    "Is it true that money can be stolen from m10 accounts?": 
        "You can fully trust m10; we operate 24/7 using the most modern defense systems. However, some users fall victim to external scammers. To stay safe, NEVER share, send, or show your bank card number, CVV code, or OTP (SMS code) to anyone. Following this simple rule protects your funds from potential risks.",
    
    "Can an m10 employee call me or contact me?": 
        "m10 employees will only contact you via the company's official email address or the official phone number 0124044114. Our staff will NEVER ask for your bank card details, CVV code, or OTP to perform any transaction. If anyone claiming to be from 'PashaPay' or 'm10' asks for this data, they are imposters. PashaPay is not responsible for losses resulting from sharing private data with third parties.",
    
    "What should I do if money has been stolen from my m10 balance?": 
        "We recommend staying vigilant with your private data. If you encounter a suspicious or fraudulent incident, take these steps immediately: 1. Block your app by calling our Call Center at *8810. 2. Report the incident to the 102 hotline or the Main Department for Combating Cybercrime. 3. Save all relevant information to assist in the investigation. Your security is our priority.",

    # Biometrics & Face ID (m10-ID)
    "Can I opt out or refuse the face recognition (biometric) verification?": 
        "No, face verification is mandatory during the initial registration process and when accessing your account from a new device.",
    
    "How is my biometric data used and stored?": 
        "Your facial data is used exclusively for identity verification purposes and will never be shared with any third parties.",
    
    "Is m10-ID available for all devices? What are the requirements?": 
        "m10-ID is available for all Android and iOS mobile devices equipped with a front-facing camera.",
    
    "What happens if someone has facial features similar to mine (e.g., a twin)?": 
        "Due to highly similar facial structures, identical twins may occasionally pass the verification. However, for the vast majority of users, our algorithm is capable of distinguishing between similar-looking individuals.",
    
    "In which cases do I need to perform face recognition again?": 
        "You will be required to complete face verification in the following scenarios: 1. When logging into your m10 account from a different device. 2. If you log out and log back in on the same device. 3. If the m10 application is deleted and re-installed."
}

class HybridChatbot:
    """
    FAQ Chatbot implementing Hybrid Search:
    Combines Dense Retrieval (SBERT) and Sparse Retrieval (BM25) 
    using Reciprocal Rank Fusion (RRF).
    """
    def __init__(self, questions: List[str], answers: List[str]):
        self.questions = questions
        self.answers = answers

        print('Initializing Vector Embeddings...')
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.question_embeddings = self.encoder.encode(questions)

        print('Initializing BM25 Search...')
        tokenized_corpus = [q.lower().replace('?', '').replace('!', '').split() for q in questions]
        self.bm25 = bm25s.BM25()
        self.bm25.index(tokenized_corpus)

    def get_dense_top_k(self, query: str, k: int = TOP_K_CANDIDATES) -> np.ndarray:
        """Retrieve top K documents based on semantic similarity."""
        query_vec = self.encoder.encode([query])
        similarities = np.dot(query_vec, self.question_embeddings.T)[0]
        return np.argsort(similarities)[::-1][:k]

    def get_sparse_top_k(self, query: str, k: int = TOP_K_CANDIDATES) -> np.ndarray:
        """Retrieve top K documents based on keyword matching."""
        tokenized_query = query.lower().replace('?', '').replace('!', '').split()
        indices, _ = self.bm25.retrieve([tokenized_query], k=k)
        return indices[0]

    def rrf_combine(self, dense_indices: np.ndarray, sparse_indices: np.ndarray) -> List[Tuple[int, float]]:
        """Combines two sets of rankings using Reciprocal Rank Fusion."""
        scores = {}
        for rank, idx in enumerate(dense_indices):
            scores[idx] = scores.get(idx, 0) + 1 / (RRF_K + rank + 1)

        for rank, idx in enumerate(sparse_indices):
            scores[idx] = scores.get(idx, 0) + 1 / (RRF_K + rank + 1)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def ask(self, query: str) -> str:
        if len(query.split()) < 2:
            return "Could you please provide a bit more detail? I need a full question to help you better."

        dense_top = self.get_dense_top_k(query)
        sparse_top = self.get_sparse_top_k(query)
        combined = self.rrf_combine(dense_top, sparse_top)

        if not combined:
            return "I'm sorry, I couldn't find any answer."

        best_idx, rrf_score = combined[0]
        query_vec = self.encoder.encode([query])
        actual_similarity = np.dot(query_vec, self.question_embeddings[best_idx].T)[0].item()

        if actual_similarity < SIMILARITY_THRESHOLD:
            return "I'm sorry, I don't have enough information to answer that. Please try rephrasing your question or contact support."
        return self.answers[best_idx]
        
@st.cache_resource
def load_bot():
    questions = list(faq_data.keys())
    answers = list(faq_data.values())
    return HybridChatbot(questions, answers)

st.set_page_config(
    page_title="m10 AI Assistant", 
    page_icon="🤖", 
    layout="centered"
)

st.title("⚡ m10 Smart Help")
st.markdown("""
Get instant, precise answers about your digital wallet, security protocols, and m10-ID verification.
""") 
st.divider()

bot = load_bot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching for the best answer..."):
            response = bot.ask(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
