import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DATA_DIR = "data"
CHROMA_PATH = "chroma_db"

def get_embedding_model():
    """Returns the free, local HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store():
    """Loads PDFs, chunks them, and builds the Chroma database."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created '{DATA_DIR}' directory. Put PDFs here.")
        return None
        
    print(f"Loading PDFs from '{DATA_DIR}'...")
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()
    
    if not documents:
        print("⚠️ No PDFs found in the data/ directory. Skipping database build.")
        return None
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    print(f"Building local Vector DB with {len(chunks)} chunks...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=get_embedding_model(),
        persist_directory=CHROMA_PATH
    )
    print("✅ Vector DB successfully built!")
    return db

def get_vector_store():
    """Retrieves the existing Vector DB."""
    if os.path.exists(CHROMA_PATH):
        return Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_model())
    return None

if __name__ == "__main__":
    build_vector_store()