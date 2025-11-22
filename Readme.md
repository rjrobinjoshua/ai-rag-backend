🚀 AI Backend — FastAPI + OpenAI

This project is a lightweight AI backend built with FastAPI, designed as part of my 10-week AI Engineering learning roadmap.
It includes basic endpoints, OpenAI integration, and a clean, scalable folder structure.

📂 Project Structure
ai-backend/
│
├── api/
│   └── routes/
│       ├── health.py
│       ├── ask.py
│       └── embed.py
│
├── services/
│   └── openai_service.py
│
├── core/
│   ├── config.py
│   ├── logging.py
│   └── errors.py
│
├── tests/
├── app.py
├── requirements.txt
├── .env
└── README.md

🔧 Setup Instructions
1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Add your OpenAI API key

Create a .env file:

OPENAI_API_KEY=your_key_here

▶️ Run the Server
uvicorn app:app --reload


Now open:

http://localhost:8000/health
 → Health check

POST /ask → Ask a question

POST /embed → Generate embeddings

🧪 Testing (upcoming)

Basic test files can be added under:

tests/


Run tests with:

pytest

🐳 Docker (upcoming)

Build:

docker build -t ai-backend .


Run:

docker run -p 8000:8000 ai-backend