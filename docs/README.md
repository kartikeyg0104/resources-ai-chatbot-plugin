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

## Getting Started

For the setup you can follow [Setup Guide](setup.md).

To quickly start in the root directory a `Makefile` contains many ready-to-go targets, that allow to run basic flows(e.g. running the API).

In this doc file we'll use these targets, without going into the details of the scripts and of the implementation reasonings. For further information you can visit the package-related doc files.

## Data Pipeline

The first thing we want to be able to do is running the whole data pipeline. The data pipeline comprehends the following phases:
- Data Collection
- Preprocessing
- Chunking
- Embedding
- Storage

So starting from the identificatiion of the data sources(e.g. Jenkins Official Documentation) the data pipeline will collect it, process it, and finally store it in a vector database(FAISS) to later perform semantic search.

To run the following pipeline you can use the `run-data-pipeline` target:
```bash
make run-data-pipeline
```

> **Note:** for more details on the scripts and on the single processes you can visit the docs under `docs/chatbot-core/data/` and `docs/chatbot-core/rag/`.

## API

This section documents the API component of the chatbot. It exposes the functionality as a RESTful service using FastAPI.

## User Interface
