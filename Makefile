.PHONY: all api setup-backend run-api build-frontend test run-frontend-tests run-backend-tests

all: setup-backend run-api build-frontend api test run-frontend-tests run-backend-tests

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

run-api:
	cd chatbot-core && \
	. venv/bin/activate && \
	PYTHONPATH=$$(pwd) uvicorn api.main:app --reload

api: setup-backend run-api

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
