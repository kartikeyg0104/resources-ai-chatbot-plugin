.PHONY: all api setup-backend build-frontend test data-collection

all: build-frontend setup-backend run-api

setup-backend:
	if [ ! -d chatbot-core/venv ]; then \
		cd chatbot-core && \
		python3 -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt; \
	else \
		echo "Backend already set up. Skipping virtualenv creation and dependencies installation."; \
	fi

build-frontend:
	cd frontend && \
	npm install && \
	npm run build

# API

run-api:
	cd chatbot-core && \
	. venv/bin/activate && \
	PYTHONPATH=$$(pwd) uvicorn api.main:app --reload

api: setup-backend run-api

# TESTS

run-frontend-tests:
	cd frontend && \
	npm install && \
	echo "### RUNNING FRONTEND TESTS ###" && \
	npm run test

run-backend-tests: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### RUNNING BACKEND UNIT TESTS ###" && \
	PYTHONPATH=$$(pwd) pytest tests/unit && \
	echo "### RUNNING BACKEND INTEGRATION TESTS ###" && \
	PYTHONPATH=$$(pwd) pytest tests/integration

test: run-frontend-tests run-backend-tests

# DATA PIPELINE

## DATA COLLECTION

run-data-collection-docs: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### COLLECTING JENKINS DOCS ###" && \
	python3 data/collection/docs_crawler.py

run-data-collection-plugins: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### COLLECTING JENKINS PLUGIN DOCS ###" && \
	echo "### 1. FETCHING PLUGIN NAMES LIST ###" && \
	python3 data/collection/fetch_list_plugins.py && \
	echo "### 2. FETCHING PLUGIN DOCS ###" && \
	python3 data/collection/jenkins_plugins_fetch.py

run-data-collection-discourse: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### COLLECTING DISCOURSE THREADS ###" && \
	echo "### 1. FETCHING DISCOURSE TOPICS ###" && \
	python3 data/collection/discourse_topics_retriever.py && \
	echo "### 2. FILTERING DISCOURSE TOPICS ###" && \
	python3 data/collection/collection_utils/filter_discourse_threads.py && \
	echo "### 3. FETCHING DISCOURSE POSTS FOR FILTERED TOPICS ###" && \
	python3 data/collection/discourse_fetch_posts.py

data-collection: run-data-collection-docs run-data-collection-plugins run-data-collection-discourse

## DATA PREPROCESSING

run-data-preprocessing-docs: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### PREPROCESSING JENKINS DOCS ###" && \
	echo "### 1. PROCESSING JENKINS DOCS ###" && \
	python3 data/preprocessing/preprocess_docs.py && \
	echo "### 2. FILTERING PROCESSED JENKINS DOCS ###" && \
	python3 data/preprocessing/filter_processed_docs.py

run-data-preprocessing-plugins: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### PREPROCESSING JENKINS PLUGIN DOCS ###" && \
	python3 data/preprocessing/preprocess_plugin_docs.py

data-preprocessing: run-data-preprocessing-docs run-data-preprocessing-plugins

## DATA CHUNKING

run-data-chunking-docs: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### CHUNKING JENKINS DOCS ###" && \
	python3 data/chunking/extract_chunk_docs.py

run-data-chunking-plugins: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### CHUNKING JENKINS PLUGIN DOCS ###" && \
	python3 data/chunking/extract_chunk_plugins.py

run-data-chunking-discourse: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### CHUNKING DISCOURSE THREADS ###" && \
	python3 data/chunking/extract_chunk_discourse.py

run-data-chunking-stack: setup-backend
	cd chatbot-core && \
	. venv/bin/activate && \
	echo "### CHUNKING STACKOVERFLOW THREADS ###" && \
	python3 data/chunking/extract_chunk_stack.py

data-chunking: run-data-chunking-docs run-data-chunking-plugins run-data-chunking-discourse run-data-chunking-stack
