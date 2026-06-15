import streamlit as st
import requests


st.set_page_config(
    page_title="AegisRAG",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AegisRAG")
st.subheader("Chat with your PDFs")
if "messages" not in st.session_state:
    st.session_state.messages = []
response = requests.get(
    "http://127.0.0.1:8000/documents"
)

documents = response.json()["documents"]

selected_doc = st.selectbox(
    "Select Document",
    documents
)
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# Upload to FastAPI
if uploaded_file is not None:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    response = requests.post(
        "http://127.0.0.1:8000/upload",
        files=files
    )

    if response.status_code == 200:
        st.success(f"Uploaded: {uploaded_file.name}")

question = st.chat_input(
    "Ask a question about your document..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                "question": question,
                "source": selected_doc
                }
            )

            st.write("Status Code:", response.status_code)
            st.write("Response Text:", response.text)

            result = response.json()

            answer = result["answer"]

        st.markdown(answer)

        st.markdown("**Sources**")

        for source in result["sources"]:
            st.write(f"📄 {source}")