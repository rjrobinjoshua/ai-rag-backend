🚀 AI Backend — FastAPI + OpenAI

A lightweight, production-ready backend for LLM-powered applications

<p align="center"> <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/FastAPI-🚀-009688?style=for-the-badge" /> <img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge" /> <img src="https://img.shields.io/badge/Docker-ready-0db7ed?style=for-the-badge" /> <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" /> </p>

A clean and structured backend that powers LLM features such as chat, embeddings, and RAG.
Built during a 10-week AI Engineering roadmap.

📁 Project Structure
- `api/` → FastAPI routes
- `services/` → business logic
- `core/` → config, constants
- `models/` → request/response models

🛠️ Setup Instructions
1️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your OpenAI API Key

Create a .env file:

OPENAI_API_KEY=your_key_here
CHATGPT_MODEL=gpt-4.1-mini

▶️ Run the Server
uvicorn app.main:app --reload


Visit:

GET http://localhost:8000/health
 → Health Check

POST http://localhost:8000/ask
 → Ask a question

POST http://localhost:8000/embed
 → Generate embeddings

🔌 API Endpoints
🩺 Health Check
GET /health


Returns:

{ "status": "ok" }

💬 Ask the LLM
POST /ask
{
  "question": "What is Docker?"
}

🧠 Embeddings
POST /embed
{
  "text": "FastAPI is great."
}

🧪 Testing

Add tests under:

tests/


Run them with:

pytest

🐳 Docker Support

Build:

docker build -t ai-backend .


Run:

docker run -p 8000:8000 ai-backend

📘 Notes

Designed to scale into a full RAG + Agents backend.

This project is Week 1 deliverable of a 10-week AI Engineering plan.

Additional features coming: cost optimization, async, multi-model routing, agentic workflows.

🙌 Credits

Built by Robinjoshua Parthiban,
as part of a disciplined journey toward becoming an AI Engineer.