import streamlit as st
import os
from utils import configure_page, breaks, file_uploader, file_remover
from mylogging import configure_logging, toggle_logging, display_logs
from collections_setup import initialize_chromadb, initialize_collection, update_collection, get_database_directory
from ollama_setup import is_ollama_running, get_relevant_text, generate_answer, get_contextual_prompt

if __name__ == "__main__":

    configure_page()
    st.markdown("<h1 style='text-align: center;'>Streamlit RAG</h1>", unsafe_allow_html=True)
    breaks(2)
    st.write(
        """
        Welcome to this Streamlit app that demonstrates how to integrate the Retrieval-Augmented Generation (RAG) model with ChromaDB and Ollama.
        
        With this app, you can:
        - Upload multiple text files to build a contextual knowledge base,
        - Enter a custom prompt to generate a response, and
        - Generate a response using the RAG model.
        
        **Note:** This app currently runs only on a local machine.
        """
    )
    breaks(1)
    
    # # Disable Chroma telemetry
    # os.environ["CHROMA_TELEMETRY_ENABLED"] = "False"
    
    # Initialize logger
    logger, log_stream = configure_logging()
    st.markdown(
        """
        <style>
        /* This targets the selectbox container */
        div[data-baseweb="select"] {
            max-width: 150px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    ) 
    logging_level = st.selectbox("Select logging level", ['INFO', 'DEBUG', 'WARNING'], index=2)
    toggle_logging(logging_level, logger)
    st.divider()

    # ---- Vector Store Setup ----
    # Initialize ChromaDB and collection
    breaks(1)
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  
    client, embedding_func = initialize_chromadb(EMBEDDING_MODEL)
    collection_name = "my_collection"
    collection = initialize_collection(client, embedding_func, collection_name)

    # Define the directory for storing uploaded file names
    database_dir = get_database_directory()
    UPLOADED_FILES_LOG = os.path.join(database_dir, "uploaded_files.txt")

    # Function to load the list of uploaded files
    def load_uploaded_files():
        if os.path.exists(UPLOADED_FILES_LOG):
            with open(UPLOADED_FILES_LOG, "r") as f:
                return f.read().splitlines()
        return []

    # Function to save the list of uploaded files
    def save_uploaded_files(file_list):
        with open(UPLOADED_FILES_LOG, "w") as f:
            f.write("\n".join(file_list))

    # # Function to remove a file and its associated vectors
    # def remove_file_and_vectors(file_name, collection):
    #     # Remove the file from the session state
    #     st.session_state.uploaded_files = [f for f in st.session_state.uploaded_files if f != file_name]
        
    #     # Save the updated list of uploaded files
    #     save_uploaded_files(st.session_state.uploaded_files)
        
    #     # Remove the associated vectors from the database
    #     collection.delete(where={"filename": file_name})

    def remove_file_and_vectors(file_name, collection):
        """
        Remove a file and its associated vectors from the database.
        """
        # Remove the file from the session state
        st.session_state.uploaded_files = [f for f in st.session_state.uploaded_files if f != file_name]
        
        # Save the updated list of uploaded files
        save_uploaded_files(st.session_state.uploaded_files)
        
        # Remove the associated vectors from the database
        try:
            # Delete vectors where the metadata field "source" matches the file name
            collection.delete(where={"source": file_name})
            st.success(f"Successfully removed {file_name} and its vectors from the database.")
        except Exception as e:
            st.error(f"Failed to remove vectors for {file_name}: {e}")

    # Upload files
    _, col, _ = st.columns([.2, .4, .2])
    with col:
        st.markdown(
            '<h3 style="text-align: center;">Drag and drop or click to upload multiple files:</h3>',
            unsafe_allow_html=True
        )
        uploaded_files = file_uploader()
        st.write(
            "Uploaded files are processed to build a contextual knowledge base for the RAG model. "
            "When you submit a prompt, the model retrieves relevant information from these documents to generate more accurate and context-aware responses."
        )

    # Get the current uploaded filenames
    current_uploaded_filenames = [file.name for file in uploaded_files] if uploaded_files else []
    logger.debug(f"\n\t-- Currently uploaded files:")
    logger.debug(current_uploaded_filenames)

    # Load the previously uploaded files
    previously_uploaded_files = load_uploaded_files()
    st.write(f"Previously uploaded files: {previously_uploaded_files}")

    # Update the session state with the new uploaded files
    st.session_state.uploaded_files = list(previously_uploaded_files)
    st.write(f"Updated uploaded files: {st.session_state.uploaded_files}")

    # Update collection with uploaded files
    collection, updated_session_state = update_collection(
        collection, uploaded_files, st.session_state["uploaded_files"]
    )

    # Update the session state
    st.session_state["uploaded_files"] = updated_session_state
    save_uploaded_files(st.session_state["uploaded_files"])
    st.write(f"Collection count: {collection.count()}")
    st.write(f"Files in database directory: {os.listdir(get_database_directory())}")
    logger.debug(f"\n\t-- Collection data currently uploaded:")
    data_head = collection.get(limit=5)
    for i, (metadata, document) in enumerate(zip(data_head["metadatas"], data_head["documents"]), start=1):
        logger.debug(f"Item {i}:")
        logger.debug(f"Metadata: {metadata}")
        logger.debug(f"Document: {document}")
        logger.debug("-" * 40)

    # Display the list of uploaded files
    st.write("### Uploaded Files")
    for file_name in st.session_state.uploaded_files:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.write(file_name)
        with col2:
            if st.button(f"Delete {file_name}"):
                remove_file_and_vectors(file_name, collection)

    # ---- Response Generation ----
    # Ollama server details
    BASE_URL = "http://127.0.0.1:11434/api"
    MODEL = "llama3.2:1b"

    # At the beginning of your app
    if not is_ollama_running(BASE_URL, logger):
        st.error("Ollama server is not running. Please start it with 'ollama serve' before continuing.")
        st.stop()

    # Streamlit UI
    st.divider()
    col1, _, col2 = st.columns([.6, .01, 1])
    with col1:
        st.subheader("Enter your prompt:")
        query = st.text_area("", height=200)
    relevant_text = get_relevant_text(collection, query=query, nresults=2)
    logger.debug(f"\n\t-- Relevant text retrieved:")
    logger.debug(relevant_text)
    if st.button("Generate"):
        if query.strip():
            with st.spinner("Generating response..."):
                context_query = get_contextual_prompt(query, relevant_text)
                response, _ = generate_answer(BASE_URL, MODEL, context_query)
                with col2:
                    st.subheader("Response:")
                    st.text_area("", value=response, height=200)
        else:
            st.warning("Please enter a prompt.")

    display_logs(log_stream)
