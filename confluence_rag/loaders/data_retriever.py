from typing import List, Dict, Callable

from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage

from confluence_rag.loaders.utils import LLM_NAME


def load_model(model: str = LLM_NAME) -> Ollama:
    """
    Load a language model using the Ollama library.

    Args:
        model (str): The name of the model to load. Defaults to "llama3.2".

    Returns:
        Ollama: An instance of the loaded model.
    """
    return Ollama(model=model)


def load_chain(db: Chroma, llm: Ollama) -> RetrievalQA:
    """
    Create a RetrievalQA chain using the specified language model and database.

    Args:
        db (Chroma): The Chroma vector database used for document retrieval.
        llm (Ollama): The language model used for generating responses.

    Returns:
        RetrievalQA: A RetrievalQA chain configured for querying with document sources.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=True,
        verbose=True,
    )

def dicts_to_messages(messages: List[Dict[str, str]]) -> List:
    """
    Convert a list of message dictionaries into message objects for processing.

    Args:
        messages (List[Dict[str, str]]): A list of dictionaries representing messages,
                                         each with 'role' and 'content' keys.

    Returns:
        List: A list of message objects (SystemMessage, HumanMessage, AIMessage).
    """
    message_objects = []
    for message in messages:
        if message['role'] == 'system':
            message_objects.append(SystemMessage(content=message['content']))
        elif message['role'] == 'user':
            message_objects.append(HumanMessage(content=message['content']))
        elif message['role'] == 'assistant':
            message_objects.append(AIMessage(content=message['content']))
    return message_objects

def query_chain(load_chain: RetrievalQA) -> Callable:
    """
    Generate a query function that processes input messages, formats prompts, and returns a response.

    Args:
        load_chain (RetrievalQA): The RetrievalQA chain used for querying and retrieving information.

    Returns:
        function: A function that takes a message string and history, queries the chain, and returns formatted output.
    """
    def query(message: str, history: List[Dict[str,str]]) -> str:
        """
        Query the RetrievalQA chain and return the formatted result.

        Args:
            message (str): The input message from the user.
            history (List[Dict[str, str]]): The conversation history containing messages.

        Returns:
            str: The response from the chain including relevant documents.
        """
        history.append({"role": "user", "content": message})
        messages = dicts_to_messages(history)
        prompt_template = ChatPromptTemplate.from_messages(messages)
        prompt = prompt_template.format()

        response = load_chain({"query": prompt})
        source_documents = set([document.metadata["source"] for document in response["source_documents"]])
        source_lines = "\n".join(source_documents)
        output = f"""
{response["result"]}
        
**Relevant Documents**  :
{source_lines}
        """
        return output

    return query
