# 🚀 AI Backend — FastAPI + OpenAI

A lightweight, production-ready backend for LLM-powered applications.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-🚀-009688?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-ready-0db7ed?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

A clean and structured backend powering LLM features such as chat, embeddings, and (soon) RAG.
Part of a 10-week AI Engineering roadmap.

***

## ✨ Features

* **FastAPI backend** with clean modular structure
  (`api/`, `services/`, `core/`, `models/`)

* **LLM Chat Endpoint (`/ask`)**
  Uses OpenAI GPT-4.1-mini (configurable).

* **Embeddings Endpoint (`/embed`)**
  Ready for RAG ingestion + semantic search.

* **Environment-based configuration**
  `.env` for API keys + model selection.
  Cached with `lru_cache` for performance.

* **Pydantic request/response models**
  Auto-documented via Swagger & ReDoc.

* **Error-handling middleware (extendable)**
  Centralized place for logging + exceptions.

* **Loguru logging**
  Clean, timestamped logs during development.

* **Docker support**
  Build + run with production settings.

* **Auto-generated API Documentation**
  * Swagger → `/docs`
  * ReDoc → `/redoc`

# 🛠️ Setup Instructions

### **1️⃣ Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Add Your OpenAI API Key**

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
CHATGPT_MODEL=gpt-4.1-mini
```

### **4️⃣ (Recommended) Enable Pre-Commit Hooks**

Install pre-commit:

```bash
pip install pre-commit
```

Install the pre-commit hooks:

```bash
pre-commit install
```

This enables:

* Black formatting

* Ruff linting & autofix

* Test suite execution

* Protection against committing .env files

***

# ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

The server will start at:

```
http://localhost:8000
```

***

## 🔌 API Overview

The full interactive API docs are available when the server is running:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`
* OpenAPI schema: `http://localhost:8000/openapi.json`

# 🧪 Testing

Place tests under:

```
tests/
```

Run them with:

```bash
pytest
```

***

# 🐳 Docker Support

### Build:

```bash
docker build -t ai-rag-backend .
```

### Run:

```bash
docker run --rm --env-file .env -p 8000:8000 ai-rag-backend
```

***

# 🙌 Credits

Built by **Robinjoshua Parthiban**,
as part of a disciplined journey toward becoming an **AI Engineer**.

## License

This project is licensed under the MIT License.
It is a learning/testing repository created solely for educational purposes.
