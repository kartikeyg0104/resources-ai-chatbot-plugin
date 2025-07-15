# Documentation for Jenkins Chatbot Plugin

This documentation folder contains resources and instructions related to the development of the RAG-based chatbot plugin for Jenkins.

## Directory Structure

Below is a brief explanation of the key subdirectories:

- `chatbot-core/`: Core logic of the chatbot.
  - `data/`: Data-related files and scripts.
    - `collection/`: Scripts to collect data from Jenkins Docs, Jenkins Plugins, Discourse, StackOverflow.
    - `preprocessing/`: Scripts to clean, filter, the collected data before chunking.
    - `raw/`: Output directory for collected data.
    - `processed/`: Output directory for cleaned and filtered data.
  - `utils/`: Contains utils for the chatbot-core directory(e.g. logger).
  - `rag/`: Core logic of the RAG
    - `embedding/`: Scripts to embed the chunks.
    - `vectorestore/`: Scripts to store the embeddings into a vector database.
    - `retrieval/`: Scripts to perform the semantic research across the vectore database.
  - `api/`: FastAPI application that exposes the chatbot via a REST API.
    - `main.py`: Entry point to run the FastAPI app.
    - `routes/`: Defines the HTTP endpoints.
    - `services/`: Contains the business logic, representing the service layer .
    - `models/`: Contains schemas and LLM interface.
    - `prompts/`: Utilities for prompt formatting and construction.
    - `config/`: Loads and provides application configuration (YAML-based).
  - `requirements.txt`: Python dependencies.
- `docs/`: Developer documentation.
- `frontend/`: Directory for the frontend React application.

## Setup Instructions

For the setup you can follow [Setup Guide](setup.md).

> **Note**:
> Please use **Python 3.11 or later**. Ensure your installation includes support for the `venv` module.

To set up the environment and run the scripts:

1. Navigate to the `chatbot-core` directory:
    ```bash
    cd chatbot-core
    ```

2. Create a Python virtual environment
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment
    - Linux/macOS
        ```bash
        source venv/bin/activate
        ```
    - Windows
        ```bash
        .\venv\Scripts\activate
        ```
4. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```
5. Set the `PYTHONPATH` to the current directory(`chatbot-core/`):
    ```bash
    export PYTHONPATH=$(pwd)
    ```

## Data Collection

The data collection scripts are located under:

```
chatbot-core/data/collection/
```

These scripts gather information from three key sources:
- Jenkins official documentation
- Discourse community topics
- StackOverflow threads

This section describes how to run the individual data collection scripts for each source. The results will be stored in the `raw` directory.

## Data Preprocessing

After collecting raw documentation from the different sources, a preprocessing step is required to extract the main content, clean from undesired HTML tags, and remove low-value or noisy entries. This step ensures the chatbot receives clean, relevant text data.

## Chunking

After collecting and preprocessing the raw content from various sources, the next step in the RAG pipeline is **chunking**. This phase involves splitting the cleaned text into smaller, semantically meaningful units that are suitable for embedding and retrieval by the chatbot.

All chunking scripts are located under the directory:`chatbot-core/data/chunking/`


Below are the chunking procedures for each data source.

## Embedding

The embedding-related scripts are located in: `chatbot-core/rag/embedding/`

This phase converts preprocessed and chunked text documents into dense vector representations using a transformer-based model. These embeddings are later stored in a vector database to support semantic search and retrieval for the chatbot.

> **Note**: These scripts are not standalone entry points and are used as utility modules by downstream indexing and retrieval components.

## Vector Store

The vector store module is responsible for building, saving, and loading a **FAISS index** along with associated metadata for later retrieval. All logic related to persistent vector storage lives in: `chatbot-core/rag/vectorstore/`

This phase follows the **embedding** step and precedes the **retrieval** phase. It stores the document embeddings in a FAISS **IVF (Inverted File) index** to allow fast approximate nearest-neighbor search. Indeed it trade-off some accuracy for a faster retrieval.

## Retrieval

The retrieval module enables querying the FAISS vector index to find the most semantically relevant document chunks based on a natural language input. This phase is responsible for fetching context-rich results from the indexed embedding space, which are then used to inform the chatbot’s responses.

All related scripts are located under: `chatbot-core/rag/retrieval/`

## API

This section documents the API component of the chatbot. It exposes the functionality as a RESTful service using FastAPI.

## User Interface
