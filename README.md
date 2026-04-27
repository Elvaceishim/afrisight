# AfriSight — African Fintech Intelligence Platform

LLM-powered tool that ingests African fintech news, classifies signals via a LangChain + Claude pipeline, tracks experiments with MLflow, and displays results on a React dashboard.

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI + Python 3.11 |
| LLM | Anthropic Claude (claude-sonnet-4-20250514) via LangChain |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Database | Supabase (PostgreSQL) |
| Experiment tracking | MLflow |
| Frontend | React 18 + Vite + Tailwind CSS |
| Infrastructure | Docker + Docker Compose |

## Prerequisites

- Docker & Docker Compose
- A [Supabase](https://supabase.com) project
- An [Anthropic](https://console.anthropic.com) API key
- A [NewsAPI](https://newsapi.org) key

## Setup

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd afrisight
   ```

2. **Copy and fill environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your real keys
   ```

3. **Run the Supabase schema**
   - Open your Supabase project → SQL Editor
   - Paste and run `supabase_schema.sql`

4. **Start all services**
   ```bash
   docker-compose up --build
   ```

Services:
- Backend API: http://localhost:8000
- MLflow UI: http://localhost:5000
- Frontend: http://localhost:5173

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/signals` | List signals (filters: `market`, `category`, `sentiment`, `limit`) |
| GET | `/signals/{id}` | Get single signal |
| POST | `/signals` | Create signal manually |
| DELETE | `/signals/{id}` | Delete signal |
| POST | `/pipeline/run` | Trigger full ingestion + analysis pipeline |
| GET | `/pipeline/status` | Get last pipeline run status |
| GET | `/experiments` | List MLflow experiment runs |

## Running the Frontend Locally (without Docker)

```bash
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

Make sure the backend is running (either via Docker or `uvicorn app.main:app --reload` from the `backend/` directory).

## Deploying to Railway

1. Create a new Railway project
2. Add three services: Backend, MLflow, Frontend
3. Set environment variables from `.env.example` in the Backend service
4. Set `MLFLOW_TRACKING_URI` to your MLflow service's Railway URL
5. Deploy — Railway auto-detects Dockerfiles
