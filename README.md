# UrbanShield AI

Urban Intelligence & Emergency Response Platform — NioHack 2026

## Quick Start

### Backend (Python/FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit with your Supabase credentials (optional)
uvicorn main:app --reload
```

Backend runs on http://localhost:8000

### Frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:5173

### Supabase (optional)

1. Create a Supabase project
2. Run `backend/schema.sql` in the SQL editor
3. Copy URL and anon key to `backend/.env`

The app works without Supabase (demo mode with in-memory data).

## Architecture

```
Simulated IoT Sensors
        ↓
FastAPI Backend (port 8000)
        ↓
Risk / Anomaly Engine
        ↓
Incident Detection
        ↓
AI Response Layer (deterministic fallback)
        ↓
React Command Center (port 5173)
        ↓
Supabase PostgreSQL (optional)
```

## Tech Stack

- **Frontend**: React, Vite, Recharts
- **Backend**: Python, FastAPI
- **Database**: Supabase PostgreSQL (with in-memory fallback)
- **AI**: Provider abstraction with deterministic fallback
# nio_project
