import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from utils.load_docs import load_documents
from utils.split_docs import split_text
from utils.create_and_retrieve import create_vector_db, retrieve_and_invoke
import google.generativeai as genai
from gtts import gTTS
import threading
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import pysqlite3
import sys

sys.modules['sqlite3'] = pysqlite3

# Load environment variables
load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# Initialize session state for chat history and uploaded files
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'context_history' not in st.session_state:
    st.session_state.context_history = ""

def process_question(query_text):
    if st.session_state.uploaded_files and query_text:
        with st.spinner("Processing your request..."):
            # Save uploaded files to a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                for pdf_file in st.session_state.uploaded_files:
                    with open(os.path.join(temp_dir, pdf_file.name), 'wb') as f:
                        f.write(pdf_file.getvalue())

                documents = load_documents(temp_dir)
                chunks = split_text(documents)
                vectordb = create_vector_db(chunks)

                # Retrieve and generate response
                response = retrieve_and_invoke(vectordb, query_text, st.session_state.context_history)

                # Update chat history
                st.session_state.messages.append({"role": "user", "content": query_text})
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Update context history
                st.session_state.context_history += f"\n\n---\n\nUser: {query_text}\nAssistant: {response}"

def read_aloud_async(text):
    def _play_audio():
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            tts.save(f"{temp_file.name}.mp3")
            audio = AudioSegment.from_mp3(f"{temp_file.name}.mp3")
            play(audio)

    threading.Thread(target=_play_audio).start()

def main():
    st.set_page_config(page_title="PDF Query Application", page_icon="📄", layout="wide")

    # Page header
    st.markdown("""
        <style>
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .upload-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            max-width: 80%;
            clear: both;
        }
        .user-message {
            background-color: #d1e7dd;
            color: #0f5132;
            text-align: right;
            margin-left: auto;
        }
        .assistant-message {
            background-color: #f8d7da;
            color: #721c24;
            text-align: left;
            margin-right: auto.
        }
        .message-line {
            border-top: 1px solid #ccc.
            margin: 10px 0.
        }
        .input-container {
            display: flex.
            flex-direction: column.
            align-items: center.
            margin-top: 20px.
        }
        .read-aloud {
            cursor: pointer.
            margin-left: 10px.
        }
        </style>
        <div class="header">
            <h1>PDF Query Application</h1>
            <p>Upload your PDF files and ask questions about the content.</p>
        </div>
        """, unsafe_allow_html=True)

    # File uploader
    upload_container = st.container()
    with upload_container:
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if pdf_files:
        st.session_state.uploaded_files = pdf_files
        st.session_state.messages.append({"role": "system", "content": "PDFs uploaded successfully. You can now ask questions about them."})

    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for idx, msg in enumerate(st.session_state.messages):
            if idx > 0:
                st.markdown('<div class="message-line"></div>', unsafe_allow_html=True)
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>User:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
                if st.button("🔊", key=f'read_aloud_{idx}', help="Click to read aloud"):
                    read_aloud_async(msg["content"])

    # User input
    input_container = st.container()
    with input_container:
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        query_text = st.text_input("Ask a question about the PDFs:")
        if st.button("Submit"):
            process_question(query_text)
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
