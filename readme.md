# 🚀 Streamlit RAG Code with Ollama Models and ChromaDB

---

### 🎥 Demo Video
[Watch the demo video](https://github.com/DavidePanza/streamlit_RAG/blob/main/demo_video.gif)

---

## 📌 Overview
This code provides a way to use Retrieval-Augmented Generation (RAG) with Streamlit as the user interface (UI), integrating Ollama models and ChromaDB on a local machine. It allows users to:
- Upload multiple text files to build a knowledge base which can be accessed by the LLM 
- Retrieve relevant knowledge using RAG with Ollama models 
- Generate AI-powered responses based on user queries
- Manage database size by clearing embeddings and text chunks as needed (still need to be improved)

---

## ⚙️ Installation Instructions

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

### Running the Code
```bash
streamlit run src/run.py
```

---

## 📝 Usage
1. **Upload Files:** Drag and drop or select files to build the knowledge base.
2. **Generate Response:** Enter a custom prompt and click the 'Generate Response' button.
3. **Manage Files:** Use the dropdown menu to delete files from the database as needed.

---

## ⚠️ Important Considerations
- **Database Growth:** Deleting files only removes embeddings, not text chunks, which may increase the database size over time. To prevent excessive growth, you may need to manually delete the `chroma.sqlite3` file and recreate the database.


