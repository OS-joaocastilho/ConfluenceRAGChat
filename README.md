# ConfluenceRAGChat

ConfluenceRAGChat is an open-source ChatBot designed to load data from Confluence into a vector database and answer questions based on that data without the need for fine-tuning. Leveraging the power of [LangChain](https://www.langchain.com/), [Chroma](https://www.trychroma.com/), and [Ollama](https://ollama.ai/), ConfluenceChat provides a user-friendly interface to query your organization's internal knowledge base.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Loading Data into the Vector DB](#loading-data-into-the-vector-db)
  - [Launching the Chat Interface](#launching-the-chat-interface)
- [Contributing](#contributing)
- [License](#license)

## Overview
ConfluenceChat enables organizations to query their internal Confluence documentation in a conversational manner. This tool converts Confluence data into embeddings, stores it in a vector database, and uses a language model (such as LLaMA 3.2) to respond to user queries.

## Features
- **Integration with Confluence**: Load data directly from Confluence spaces or pages.
- **Vector Database Storage**: Store and retrieve data using Chroma for efficient querying.
- **No Fine-Tuning Required**: Get answers based on your data without additional model training.
- **Web-Based Interface**: Use Gradio for an intuitive chat interface.

## Prerequisites
Before using ConfluenceRAGChat, ensure the following are installed:
- **Python 3.11 or higher**
- **[Poetry](https://python-poetry.org/docs/#installation)** (for managing dependencies)
- **Ollama** with **LLama 3.2 model**
  - Ollama should be installed and running locally. Visit [Ollama's website](https://ollama.ai/) for installation instructions.

Additionally, set up your Confluence API credentials as environment variables:
```bash
export ATLASSIAN_API_KEY="your-api-key"
export ATLASSIAN_USERNAME="your-username"
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/OS-joaocastilho/confluencechat.git
   cd confluencechat
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Ensure Ollama is running on `http://localhost:11434` and has the LLaMA 3.2 model loaded:
   ```bash
   ollama run llama3.2
   ```

## Usage

### Loading Data into the Vector DB
Before launching the chat, you must load data from Confluence into the vector database. Use the provided CLI commands to load the data:

1. **Load an entire Confluence space:**
   ```bash
   poetry run confluence-rag create --space_key CONFLUENCE_SPACE_KEY
   ```
Note: Be sure the ATLASSIAN_USERNAME has permissions to access the Confluence Space Key.

2. **Load specific Confluence pages:**
   ```bash
   poetry run confluence-rag create --page_ids PAGE_ID1 PAGE_ID2
   ```
Note: Be sure the ATLASSIAN_USERNAME has permissions to access the Confluence Space Key.


*Note*: Replace `CONFLUENCE_SPACE_KEY`, `PAGE_ID1`, `PAGE_ID2`, etc., with the relevant identifiers from your Confluence instance.

### Launching the Chat Interface
Once the data is loaded into the vector database, you can launch the chat interface:

1. Run the following command:
   ```bash
   poetry run python -m confluence_rag.presentation.interface
   ```

2. The Gradio interface will open in your browser, allowing you to interact with the chatbot and ask questions based on the loaded Confluence data.

## Contributing
We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a pull request.

Please ensure that your code follows the existing style and includes appropriate documentation.

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to reach out with any questions or suggestions. Happy coding!
```

### Explanation:
- **Overview & Features**: Describes what the project does and its core capabilities.
- **Prerequisites**: Details all required dependencies and initial setup steps, including environment variables.
- **Installation**: Explains how to set up the project using Poetry.
- **Usage**: Provides step-by-step instructions for loading data and launching the app.
- **Contributing**: Includes guidelines for community contributions.
- **License**: Mentions the project's license (assuming MIT for simplicity).

Ensure that you customize any sections as needed, including your GitHub username in the `git clone` command and linking to the actual `LICENSE` file.