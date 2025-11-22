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

---

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

---

# ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

The server will start at:

```
http://localhost:8000
```

---

# 🔌 API Endpoints

### 🩺 **Health Check**
**GET** `/health`

Example response:
```json
{ "status": "ok" }
```

---

### 💬 **Ask the LLM**
**POST** `/ask`

Request:
```json
{
  "question": "What is Docker?"
}
```

---

### 🧠 **Embeddings**
**POST** `/embed`

Request:
```json
{
  "text": "FastAPI is great."
}
```

---

# 🧪 Testing (Upcoming)

Place tests under:

```
tests/
```

Run them with:

```bash
pytest
```

---

# 🐳 Docker Support (Upcoming)

### Build:
```bash
docker build -t ai-backend .
```

### Run:
```bash
docker run -p 8000:8000 ai-backend
```

---

# 🙌 Credits

Built by **Robinjoshua Parthiban**,  
as part of a disciplined journey toward becoming an **AI Engineer**.
