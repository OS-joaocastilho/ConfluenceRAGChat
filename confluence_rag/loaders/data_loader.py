import logging

import click

from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from typing import List, Optional

from confluence_rag.settings.constants import CHROMA_DB_PATH
from confluence_rag.settings.envs import load_atlassian_api_key, load_atlassian_username
from confluence_rag.loaders.utils import OLLAMA_EMBEDDINGS, load_db

# Constants to define chunking behavior
DEFAULT_CHUNK_SIZE = 1024
DEFAULT_OVERLAP_SIZE = 64
IGNORE_CHUNKS_THRESHOLD_SIZE = 128 # Minimum size for a chunk to be considered valid

# Initialize a ConfluenceLoader instance with authentication details
CONFLUENCE_LOADER = ConfluenceLoader(
    url="https://outsystemsrd.atlassian.net/wiki",
    username=load_atlassian_username(),
    api_key=load_atlassian_api_key(),
    keep_markdown_format=True,
    keep_newlines=True
)

# Headers for splitting the document using markdown structure
HEADERS = [
    ("#", "Heading 1"),
    ("##", "Heading 2"),
    ("###", "Heading 3"),
    ("####", "Heading 4"),
    ("#####", "Headging 5"),
    ("######", "Heading 6")
]

# Define text splitters for splitting based on headers and characters
HEADER_TEXT_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS
)
CHAR_TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=DEFAULT_CHUNK_SIZE,
    chunk_overlap=DEFAULT_OVERLAP_SIZE,
)

def load_confluence_pages(page_ids: List[int]):
    """
    Load pages from Confluence based on provided page IDs.

    Args:
        page_ids (List[int]): List of Confluence page IDs to load.

    Returns:
        List[Document]: A list of documents loaded from the specified page IDs.
    """
    return CONFLUENCE_LOADER.load(
        page_ids=page_ids
    )

def load_confluence_space(space_key: str):
    """
    Load all documents from a specified Confluence space.

    Args:
        space_key (str): The key identifying the Confluence space to load.

    Returns:
        List[Document]: A list of documents from the specified Confluence space.
    """
    return CONFLUENCE_LOADER.load(
        space_key=space_key
    )

def split_text(documents: List[Document]) -> List[Document]:
    """
    Split the content of documents into smaller chunks using both header and character-based splitting.
    Filters out chunks smaller than a specified threshold.

    Args:
        documents (List[Document]): List of documents to split.

    Returns:
        List[Document]: A list of document chunks that meet the size threshold.
    """
    chunks = [] # List to hold all valid chunks
    for doc in documents:
        # Split document by headers
        doc_header_chunks = HEADER_TEXT_SPLITTER.split_text(doc.page_content)
        for idx in range(len(doc_header_chunks)):
            # Ensure metadata is preserved in each chunk
            doc_header_chunks[idx].metadata = doc_header_chunks[idx].metadata | doc.metadata
        # Further split chunks by character length
        doc_chunks = CHAR_TEXT_SPLITTER.split_documents(doc_header_chunks)
        # Filter out chunks smaller than the threshold
        cleaned_chunks = [chunk for chunk in doc_chunks if len(chunk.page_content) >= IGNORE_CHUNKS_THRESHOLD_SIZE]
        chunks.extend(cleaned_chunks)  # Add valid chunks to the list
    return chunks


def persist_data(chunks: List[Document], load_existent: bool = False) -> Chroma:
    """
    Persist the processed document chunks to the Chroma vector database.

    Args:
        chunks (List[Document]): List of document chunks to persist.
        load_existent (bool): Flag indicating whether to load an existing database or create a new one.

    Returns:
        Chroma: An instance of the Chroma vector database containing the persisted data.
    """
    if load_existent:
        # Load an existing database and add new documents
        db: Chroma = load_db()
        return db.from_documents(chunks, persist_directory=CHROMA_DB_PATH, embedding=OLLAMA_EMBEDDINGS)
    else:
        # Create a new database from the chunks
        return Chroma.from_documents(chunks, persist_directory=CHROMA_DB_PATH, embedding=OLLAMA_EMBEDDINGS)

def create_vector_db(space_key: Optional[str], page_ids: Optional[List[int | str]], load_existent: bool) -> Chroma:
    """
    Load data from Confluence, process it, and persist it into the Chroma vector database.

    Args:
        space_key (Optional[str]): The key for the Confluence space to load (if provided).
        page_ids (Optional[List[int | str]]): A list of Confluence page IDs to load (if provided).
        load_existent (bool): Flag indicating whether to load an existing database or create a new one.

    Returns:
        Chroma: An instance of the Chroma vector database containing the stored data.
    """
    if space_key:
        logging.info("Loading Confluence Space...")
        documents = load_confluence_space(space_key=space_key)
    elif page_ids:
        logging.info("Loading Confluence pages...")
        documents = load_confluence_pages(page_ids=page_ids)
    else:
        logging.error("A Space key or a list of page IDs must be provided!")
        exit(1)

    # Split documents into chunks
    logging.info("Processing information...")
    chunks = split_text(documents=documents)

    # Store chunks in the vector database
    logging.info("Storing info in Vector DB")
    db = persist_data(chunks, load_existent=load_existent)
    return db
@click.group()
def cli():
    """
    CLI group definition for Confluence data processing and storage operations.
    """
    pass

@cli.command("create")
@click.option("--space_key", help="Confluence Space")
@click.option("--page_ids", multiple=True, default=[], help="Confluence Page ID (can be multiple)")
def create(space_key: Optional[str], page_ids: Optional[List[int | str]]) -> Chroma:
    """
    CLI command to create a new vector database from Confluence data.

    Args:
        space_key (Optional[str]): The key for the Confluence space.
        page_ids (Optional[List[int | str]]): List of page IDs to load data from.
    """
    return create_vector_db(space_key=space_key,
                     page_ids=page_ids,
                     load_existent=False)

@cli.command("update")
@click.option("--space_key", help="Confluence Space")
@click.option("--page_ids", multiple=True, default=[], help="Confluence Page ID (can be multiple)")
def update(space_key: Optional[str], page_ids: Optional[List[int | str]]) -> Chroma:
    """
    CLI command to update an existing vector database with new Confluence data.

    Args:
        space_key (Optional[str]): The key for the Confluence space.
        page_ids (Optional[List[int | str]]): List of page IDs to load data from.
    """
    return create_vector_db(space_key=space_key,
                     page_ids=page_ids,
                     load_existent=True)