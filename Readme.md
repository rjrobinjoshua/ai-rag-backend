![Python Version](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009485?logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange?logo=openai)
![Docker](https://img.shields.io/badge/Docker-ready-0db7ed?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)


A lightweight backend built with FastAPI, integrating OpenAI models with a clean, scalable architecture.
Part of a structured 10-week AI Engineering Roadmap.

📁 Project Structure
ai-backend/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── health.py
│   │       ├── ask.py
│   │       └── embed.py
│   │
│   ├── services/
│   │   └── openai_service.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── ask_request.py
│   │   └── ask_response.py
│   │
│   └── main.py
│
├── tests/
├── requirements.txt
├── .env
└── README.md

⚙️ Setup Instructions
1️⃣ Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your OpenAI API Key

Create .env:

OPENAI_API_KEY=your_openai_api_key_here


Get your key from:
https://platform.openai.com/api-keys

▶️ Run the Server

From project root:

uvicorn app.main:app --reload


Server starts at:

http://localhost:8000

📡 Available Endpoints
Health Check
GET /health


Example Response:

{ "status": "ok" }

Ask a Question
POST /ask


Body:

{
  "question": "What is Docker?"
}


Returns an LLM-generated answer.

Generate Embeddings
POST /embed


Body:

{
  "text": "Sample text"
}


Returns embedding vector using OpenAI embedding model.

🧪 Testing (upcoming)

Test files are placed under:

tests/


Run tests:

pytest

🐳 Docker (upcoming)

A full Dockerfile and production Compose setup will be added as part of Week 1 (Weekend Task) in the roadmap.

📘 Notes

This backend is the foundation for:

RAG system

Observability + Eval Suite

Cost & Latency optimizations

Agentic AI

Slack Bot Integration

…all built in the next 10 weeks.