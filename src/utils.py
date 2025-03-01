import streamlit as st
from mylogging import configure_logging, toggle_logging, display_logs

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

def file_remover(uploaded_files, uploaded_files_names, collection, logger):
    """
    Removes files that were deleted from the uploader.
    """
    for file_name in list(uploaded_files_names):
        if file_name not in [file.name for file in uploaded_files]:
            st.write(f"file {file_name} removed")
            uploaded_files_names.remove(file_name) 
            collection.delete(where={"source": file_name})
            logger.debug(f"File {file_name} removed from collection.")
    

