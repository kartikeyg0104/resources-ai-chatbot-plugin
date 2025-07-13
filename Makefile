.PHONY: all api setup-backend run-api build-frontend

all: setup-backend run-api build-frontend

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
