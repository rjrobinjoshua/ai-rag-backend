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

### 🚀 Core Backend
- **FastAPI backend** with a clean, modular structure
  (`api/`, `services/`, `core/`, `models/`)
- **Environment-driven configuration**
  Loads from `.env` with caching for performance.
- **Structured logging with Loguru**
  Consistent, timestamped logs for debugging and observability.
- **Error-handling & request-logging middleware**
  Centralized place for tracing, exceptions, and diagnostics.

### 💬 LLM Capabilities
- **Chat endpoint (`/ask`)**
  Powered by OpenAI (configurable model).
- **Streaming chat endpoint (`/stream`)**
  Real-time token streaming support.
- **Embeddings endpoint (`/embed`)**
  Generates vector embeddings for RAG workflows.

### 📚 Retrieval-Augmented Generation (RAG)
- **Ingestion pipeline (`scripts/ingest.py`)**
  - Chunking
  - Embedding
  - Storing into ChromaDB
- **Persistent ChromaDB vector store**
  Lives in `chroma_db/` with auto-created collections.
- **RAG Query endpoint (`/rag-query`)**
  - Top-k retrieval
  - Context construction
  - LLM synthesis
  - Source citations

### 📄 Document Handling
- **Multi-format document loader**
  Supports `.txt` and `.pdf` (via `pypdf`).
- **Text cleaning & preprocessing**
  Normalizes newlines, collapses whitespace, fixes formatting.
- **Ready for real-world ingestion**
  Works with messy, multi-page PDFs.

### 🧪 Testing
- **pytest test suite**
  - API tests
  - Service tests
  - Retrieval tests
  - RAG logic tests
- **Mock/OpenAI stubs** for offline testing.

### 🐳 Deployment
- **Docker support**
  Production-ready image build.
- **FastAPI auto-generated documentation**
  - Swagger UI → `/docs`
  - ReDoc → `/redoc`


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
