import pytest
from src.vector_store import get_embedding_model
from src.rag_tool import logistics_document_search
from src.agent import run_agent

def test_embedding_model_initializes():
    """Tests if the HuggingFace model can be loaded without errors."""
    model = get_embedding_model()
    assert model is not None

def test_tools_exist():
    """Tests if our Langchain Tools are properly decorated and importable."""
    assert logistics_document_search.name == "logistics_document_search"
    assert logistics_document_search.description is not None

def test_agent_function_exists():
    """Ensures the agent runner function is accessible."""
    assert callable(run_agent)