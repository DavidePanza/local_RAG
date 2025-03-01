import streamlit as st
import tempfile
import chromadb
import fitz 
from chromadb.utils import embedding_functions
import requests
from mylogging import configure_logging, toggle_logging, display_logs
from text_processing import lines_chunking, paragraphs_chunking

@st.cache_resource
def get_temp_dir():
    """
    Get a temporary directory.
    """
    return tempfile.TemporaryDirectory()

def initialize_chromadb(EMBEDDING_MODEL):
    """
    Initialize ChromaDB client and embedding function.
    """
    # Create a temporary directory for storing the database
    temp_dir = get_temp_dir()
    CHROMA_DATA_PATH = temp_dir.name

    # Create a persistent client (creates a local database at CHROMA_DATA_PATH)
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

    # Initialize an embedding function (using a Sentence Transformer model)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    return client, embedding_func

def initialize_collection(client, embedding_func, collection_name):
    """
    Initialize a collection in ChromaDB.
    """
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_func,
        metadata={"hnsw:space": "cosine"},
    )

    return collection

def update_collection(collection, uploaded_files):
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state["uploaded_files"]:
            st.session_state["uploaded_files"].append(uploaded_file.name)  # Track uploaded file
            
            # Read file content
            if uploaded_file.type == "text/plain":  # Handling TXT files
                file_text = uploaded_file.getvalue().decode("utf-8")
            elif uploaded_file.type == "application/pdf":  # Handling PDFs
                pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
                file_text = "\n".join([page.get_text("text") for page in pdf_document])
            else:
                file_text = ""

            # Tokenize text into chunks
            max_words = 200
            chunks = lines_chunking(file_text, max_words=max_words)

            # Store chunks in the collection
            filename = uploaded_file.name
            collection.add(
                documents=chunks,
                ids=[f"id{filename[:-4]}.{j}" for j in range(len(chunks))],
                metadatas=[{"source": filename, "part": n} for n in range(len(chunks))],
            )
        else:
            continue

    return collection