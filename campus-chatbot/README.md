# Campus Info Chatbot — Scaffold (Track A + Optional Fullstack)

This repository contains a scaffold for an Interactive Campus Info Chatbot.
It includes a Python backend (FastAPI + LangChain) and a minimal React frontend, plus a small Streamlit app scaffold for quick experiments.

Quick start (Python + Frontend)

Prerequisites: Python 3.10+, Node.js (for frontend)

1. Create a Python venv and activate it.

   PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Set required env vars (example for OpenAI):

   PowerShell (temporary for session):
   ```powershell
   $env:OPENAI_API_KEY = "your_api_key"
   ```

   Or copy `.env.example` to `.env` and fill values.

3. Build the FAISS index from the sample handbook:

   ```powershell
   python -c "from backend.ingest import ingest_text_file; ingest_text_file('sample_data/handbook.txt','faiss_index')"
   ```

4. Start the backend API (uses `OPENAI_API_KEY` if set):

   ```powershell
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```

5. Start the frontend (optional; needs Node):

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

What this scaffold contains

- `app.py` — Streamlit UI skeleton for quick local chat experiments
- `backend/main.py` — FastAPI endpoints for query handling
- `backend/ingest.py` — document ingestion + FAISS indexing functions
- `backend/ingest_mysql.py` — ingestion helper that records metadata to SQL
- `backend/llm.py` — LLM wrapper (uses OpenAI when `OPENAI_API_KEY` is set)
- `backend/scraper.py` — basic BeautifulSoup page fetcher
- `backend/db.py` — SQLAlchemy schema + helper functions for metadata
- `frontend/` — minimal React+Vite chat UI
- `sample_data/handbook.txt` — sample handbook text

OpenAI setup

To enable concise, LLM-generated answers set the `OPENAI_API_KEY` environment variable (or copy `.env.example` to `.env` and fill values). If `OPENAI_API_KEY` is not set the backend will return a short context excerpt instead of an LLM answer so you can test without keys.

API notes

- Backend endpoints: `/query` and `/api/query` (the latter is an alias used by the frontend).
- The frontend (by default) calls `http://127.0.0.1:8000/api/query` — change the URL in `frontend/src/App.jsx` if you need a different host/port.
- CORS is enabled for common local dev origins.

Next steps

- Add your campus PDFs and web pages into `sample_data/` and run the ingestion to build the vector store (`faiss_index`).
- Extend `backend/scraper.py` to crawl your official site and save pages as text documents.
- If you want persistent metadata, configure `DATABASE_URL` and use `backend/ingest_mysql.py` which records documents into the SQL table.

Help & Troubleshooting

- If you see the `(No OPENAI_API_KEY set)` fallback, set `OPENAI_API_KEY` and restart the backend.
- For frontend CORS issues, ensure the backend is running on `127.0.0.1:8000` or update the allowed origins in `backend/main.py`.

License & Notes

This scaffold is provided for educational use within your project. Customize components for your Track A or Track B requirements.
