from langchain_core.tools import tool
from src.vector_store import get_vector_store

@tool
def logistics_document_search(query: str) -> str:
    """
    Use this tool to search for internal logistics policies, company manuals, bills of lading, and proprietary data.
    Input should be a specific search query.
    """
    db = get_vector_store()
    if not db:
        return "Error: Database not initialized or no documents available. Please upload documents first."
    
    # Performing similarity search
    results = db.similarity_search(query, k=3)
    if not results:
        return "No relevant information found in internal logistics documents."
    
    # Combining the retrieved chunks into a single text block
    context = "\n\n---\n\n".join([doc.page_content for doc in results])
    return context