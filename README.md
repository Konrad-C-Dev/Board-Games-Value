# Board Games Value — Minimal Scraper + API + Frontend

This repository contains a minimal implementation of the project described in `AGENTS.md`.

## Setup and Installation

1. Create and activate a Python virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # On Windows PowerShell
# Or if you prefer not to change execution policy:
# .venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust if needed:
```powershell
copy .env.example .env
```

## Running the Application

1. Start the FastAPI backend (in the project root directory):
```powershell
# Make sure you're in the project root (Board-Games-Value folder)
cd C:\READY4AI\Board-Games-Value
$env:PYTHONPATH = "."
.venv\Scripts\python.exe -m uvicorn api.main:app --reload
```

2. In a separate terminal, start the Streamlit frontend:
```powershell
cd C:\READY4AI\Board-Games-Value
$env:PYTHONPATH = "."
.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

The backend will run on http://127.0.0.1:8000 and the frontend on http://localhost:8501

## Development

Run tests:
```powershell
python -m pytest
```

## Project Structure

- `api/` - FastAPI backend
- `db/` - SQLAlchemy models and database setup
- `scraper/` - Web scraping logic
- `utils/` - Helper utilities
- `frontend/` - Streamlit UI
- `tests/` - pytest test suite
