from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import Chroma

from confluence_rag.settings.constants import CHROMA_DB_PATH

# Model to use for generating embeddings
LLM_NAME = "llama3.2"
OLLAMA_URL = "http://localhost:11434"

# Initialize an embedding function using the Ollama library with a specified model and base URL.
OLLAMA_EMBEDDINGS = OllamaEmbeddings(
    model=LLM_NAME,
    base_url=OLLAMA_URL # URL of the local Ollama server
)

def load_db() -> Chroma:
    """
    Load a Chroma vector database using the specified embedding function and persist directory.

    Returns:
        Chroma: An instance of the Chroma vector database.
    """
    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=OLLAMA_EMBEDDINGS
    )
    return db