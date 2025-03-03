import streamlit as st
from mylogging import configure_logging, toggle_logging, display_logs
import os

def configure_page() -> None:
    """
    Configures the Streamlit page.
    """
    st.set_page_config(page_title="myRAG", 
                       layout="wide", 
                       page_icon=":rocket:")

def breaks(n=1):
    """
    Creates a line break.
    """
    if n == 1:
        st.markdown("<br>",unsafe_allow_html=True)
    elif n == 2:
        st.markdown("<br><br>",unsafe_allow_html=True)
    elif n == 3:
        st.markdown("<br><br><br>",unsafe_allow_html=True)
    else:
        st.markdown("<br><br><br><br>",unsafe_allow_html=True)

def file_uploader() -> None:
    """
    Uploads multiple files.
    """
    uploaded_files = st.file_uploader(
        "",
        type=["txt", "pdf"], 
        accept_multiple_files=True  
    )
    
    return uploaded_files

# Function to load the list of uploaded files
def load_uploaded_files(uploaded_files_log):
    if os.path.exists(uploaded_files_log):
        with open(uploaded_files_log, "r") as f:
            return f.read().splitlines()
    return []

# Function to save the list of uploaded files
def save_uploaded_files(file_list, uploaded_files_log):
    with open(uploaded_files_log, "w") as f:
        f.write("\n".join(file_list))

def remove_file_and_vectors(file_name, collection, uploaded_files_log):
    """
    Remove a file and its associated vectors from the database.
    """
    # Remove the file from the session state
    st.session_state.uploaded_files = [f for f in st.session_state.uploaded_files if f != file_name]
    
    # Save the updated list of uploaded files
    save_uploaded_files(st.session_state.uploaded_files, uploaded_files_log)
    
    # Remove the associated vectors from the database
    try:
        # Delete vectors where the metadata field "source" matches the file name
        collection.delete(where={"source": file_name})
        st.success(f"Successfully removed {file_name} and its vectors from the database.")
    except Exception as e:
        st.error(f"Failed to remove vectors for {file_name}: {e}")


