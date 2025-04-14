import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from backend.rag_retriever import create_faiss_db


# Ingest documents and create FAISS DB
if __name__ == "__main__":
    print("📄 Ingesting documents and creating FAISS DB...")
    create_faiss_db()
    print("FAISS DB creation completed!")
