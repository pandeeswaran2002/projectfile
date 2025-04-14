from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import os
from pathlib import Path

# Directory to persist the FAISS index
FAISS_DIR = "faiss_index"

# Function to create FAISS index
def create_faiss_db():
    pdf_directory = "data/knowledge_base/"
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

    documents = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

    # Create embeddings
    embeddings = OpenAIEmbeddings()

    # Split documents into chunks (if necessary, based on your documents)
    text_chunks = [doc.page_content for doc in documents]

    # Create FAISS index
    print("Creating FAISS index...")
    faiss_index = FAISS.from_texts(text_chunks, embeddings)

    # Save the FAISS index to the directory
    print(f"Saving FAISS index to {FAISS_DIR}...")
    faiss_index.save_local(FAISS_DIR)

    print("FAISS index created and saved!")
