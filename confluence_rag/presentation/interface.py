import gradio as gr

from confluence_rag.loaders.data_retriever import load_model, load_chain, query_chain
from confluence_rag.loaders.utils import load_db

# Load the Chroma vector database using the utility function
db = load_db()

# Load the language model using the specified default or configured model
llm = load_model()

# Create an interactive Gradio chat interface
# Pass the query function created by `query_chain` which wraps the `load_chain` function
# `type="messages"` ensures the interface works with a message-based input/output format
interface = gr.ChatInterface(query_chain(load_chain(db=db, llm=llm)), type="messages").launch()

# Launch the Gradio interface for interaction
interface.launch()
