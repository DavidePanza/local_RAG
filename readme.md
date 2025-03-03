# Streamlit RAG App with Ollama Models and ChromaDB

## Overview

This Streamlit app demonstrates how to integrate the Retrieval-Augmented Generation (RAG) model with Ollama models and ChromaDB on a local machine. The app allows users to upload multiple text files, generate responses using a custom prompt, and interact with a locally stored contextual knowledge base.

### Features

- Upload and manage multiple text files to build a knowledge base.
- Generate context-aware responses using RAG with Ollama models.
- Manage database size by clearing embeddings and text chunks as needed.
- Minimalistic and surrealistic design elements to enhance user experience.

## Installation Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- Streamlit
- ChromaDB
- Ollama models

### Cloning the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Setting Up the Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run src/run.py
```

## Usage

1. **Upload Files:** Drag and drop or select files to build the knowledge base.
2. **Generate Response:** Enter a custom prompt and click the 'Generate Response' button.
3. **Manage Files:** Use the dropdown menu to delete files from the database as needed.

## Important Considerations

- **Database Growth:** Deleting files only removes embeddings, not text chunks, which may increase the database size over time. To prevent excessive growth, you may need to manually delete the `chroma.sqlite3` file and recreate the database.

