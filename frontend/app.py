import streamlit as st
import requests
import os
import time

# =========================
# CONFIG
# =========================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="AegisRAG",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    max-width: 95%;
}

.hero {
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        rgba(255,75,75,0.15),
        rgba(255,255,255,0.02)
    );
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
}

.hero-sub {
    font-size: 1.1rem;
    color: #9ca3af;
}

.metric-container {
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

if "avg_response_time" not in st.session_state:
    st.session_state.avg_response_time = 0

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero">

<div class="hero-title">
🛡️ AegisRAG
</div>

<div class="hero-sub">
Enterprise Knowledge Intelligence Platform
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# METRICS
# =========================

try:

    metrics = requests.get(
        f"{API_URL}/metrics"
    ).json()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Documents",
            metrics["documents"]
        )

    with col2:
        st.metric(
            "🧩 Chunks",
            metrics["chunks"]
        )

    with col3:
        st.metric(
            "❓ Queries",
            st.session_state.query_count
        )

    with col4:
        st.metric(
            "⚡ Avg Time",
            f"{st.session_state.avg_response_time:.2f}s"
        )

except Exception:
    st.warning("Unable to load metrics.")

st.divider()

# =========================
# DOCUMENTS
# =========================

try:

    response = requests.get(
        f"{API_URL}/documents"
    )

    documents = response.json()["documents"]

except Exception:

    documents = []

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.header("📚 Document Center")

    if documents:

        selected_doc = st.selectbox(
            "Select Document",
            documents
        )

    else:

        selected_doc = None

        st.warning(
            "No documents available."
        )

    st.markdown("---")

    # Track uploaded files in session
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = set()

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        # Prevent duplicate uploads on Streamlit reruns
        if uploaded_file.name not in st.session_state.uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                st.success(
                    f"Uploaded: {uploaded_file.name}"
                )

                st.session_state.uploaded_files.add(
                    uploaded_file.name
                )

                time.sleep(1)

                st.rerun()

            else:

                st.error(
                    f"upload failed: {response.text}"
                )
                st.write(
                    "status code:", response.status_code
                )

# =========================
# CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =========================
# CHAT INPUT
# =========================

question = st.chat_input(
    "Ask a question about your document..."
)

if question:

    st.session_state.query_count += 1

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        start_time = time.time()

        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": question,
                    "source": selected_doc
                }
            )

            if response.status_code != 200:

                st.error(
                    "Failed to get response from backend."
                )

            else:

                result = response.json()

                answer = result["answer"]

                elapsed = (
                    time.time() - start_time
                )

                st.session_state.avg_response_time = (
                    (
                        st.session_state.avg_response_time
                        * (
                            st.session_state.query_count - 1
                        )
                    )
                    + elapsed
                ) / st.session_state.query_count

                st.markdown(answer)

                if result.get("sources"):

                    with st.expander(
                        "📚 Sources"
                    ):

                        for source in result["sources"]:

                            st.markdown(
                                f"""
                                **📄 {source['file']}**

                                Page: **{source['page']}**  
                                Chunk: **{source['chunk_id']}**
                                """
                            )
                            
                            st.divider()

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
