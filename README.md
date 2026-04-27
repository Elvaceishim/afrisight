# AfriSight — African Fintech Intelligence Platform

AfriSight is an AI-powered signal intelligence platform that monitors African fintech news in real time. It ingests articles across key markets — Nigeria, Kenya, Tanzania, Ethiopia, and the DRC — classifies each story using a large language model, tracks every pipeline run as an ML experiment, and surfaces the results on a live dashboard.

This project was built as a hands-on way to learn the ML engineering tools that keep appearing in data and AI job listings: **MLflow**, **embeddings**, **LangChain pipelines**, **vector similarity**, and **LLM-structured output**. Every architectural decision was made to actually use these concepts, not just read about them.

**Live demo:** [afrisight-rho.vercel.app](https://afrisight-rho.vercel.app)

---

## What It Does

1. **Ingests** — Pulls the last 7 days of fintech news from NewsAPI across 10 curated keywords (M-Pesa, Flutterwave, Paystack, mobile money Africa, etc.), deduplicates by URL.
2. **Classifies** — Sends each article through a LangChain chain backed by Claude via OpenRouter. The LLM returns structured JSON: market, category, sentiment, a two-sentence summary, and a confidence score.
3. **Stores** — Persists every signal and pipeline run summary to Supabase PostgreSQL.
4. **Tracks** — Logs parameters, per-article confidence metrics, and run artifacts to MLflow for experiment comparison (local environment only; gracefully skipped in production).
5. **Displays** — Renders signals on a React dashboard with market and category filters, confidence indicators, and a one-click pipeline trigger.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
│              React + Vite + Tailwind (Vercel)               │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend (Render)                  │
│                                                             │
│  POST /pipeline/run                                         │
│    │                                                        │
│    ├── ingest.py       NewsAPI → deduplicated articles       │
│    ├── chain.py        LangChain → OpenRouter → Claude       │
│    │                   returns: market, category,            │
│    │                   sentiment, summary, confidence        │
│    └── tracker.py      MLflow experiment logging             │
│                        (graceful fallback when unavailable)  │
│                                                             │
│  GET /signals          Supabase query with filters          │
│  GET /pipeline/status  Last run metadata                    │
│  GET /experiments      MLflow run history                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┴────────────────┐
          │                                 │
┌─────────▼──────────┐           ┌──────────▼──────────┐
│  Supabase (cloud)  │           │  MLflow (local only) │
│  signals table     │           │  experiment tracking │
│  pipeline_runs     │           │  metrics + artifacts │
└────────────────────┘           └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.11 |
| LLM | Claude (anthropic/claude-sonnet-4-5) via OpenRouter |
| LLM Orchestration | LangChain (`langchain-core`, `langchain-openai`) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 *(local only)* |
| Experiment Tracking | MLflow *(local only, graceful fallback in prod)* |
| Database | Supabase (PostgreSQL) |
| News Source | NewsAPI |
| Frontend | React 18 + Vite + Tailwind CSS |
| Local Infrastructure | Docker + Docker Compose |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |

---

## ML Concepts Implemented

### MLflow — Experiment Tracking
Every pipeline run is logged as an MLflow experiment. Parameters (model name, prompt version, run ID), per-article metrics (LLM confidence score), and a final run summary artifact are all tracked. This mirrors how ML teams compare model versions and detect regressions across runs.

In production (Render), there is no MLflow server. The tracker wraps every MLflow call in a try/except — if the server is unreachable, it logs a warning and returns a fallback UUID. The pipeline continues without interruption. This is the practical difference between a research environment and a deployed system.

### Embeddings — Semantic Classification (Local)
The local environment includes a sentence-transformer classifier (`all-MiniLM-L6-v2`) that uses cosine similarity to group articles by semantic meaning. This is the same technique used in semantic search, RAG retrieval, and recommendation systems. It is intentionally excluded from the production build: the model requires more RAM than Render's free tier (512MB) provides, which is itself a real-world ML deployment constraint worth understanding.

### Structured LLM Output
The LangChain chain uses a `PromptTemplate` that instructs the LLM to return a strict JSON object — no markdown, no explanation. The output parser strips any accidental fencing and falls back to safe defaults on JSON parse failure. This pattern (structured output + graceful degradation) is standard practice in production LLM pipelines.

---

## Project Structure

```
afrisight/
├── backend/
│   ├── app/
│   │   ├── config.py           # Pydantic Settings, env var loading
│   │   ├── database.py         # Supabase singleton
│   │   ├── main.py             # FastAPI app, CORS, router registration
│   │   ├── models/
│   │   │   └── schemas.py      # Pydantic v2 models (Signal, PipelineRunResult, etc.)
│   │   ├── pipeline/
│   │   │   ├── ingest.py       # NewsAPI fetch + deduplication
│   │   │   ├── chain.py        # LangChain + OpenRouter + Claude
│   │   │   ├── classifier.py   # sentence-transformer cosine similarity (local only)
│   │   │   └── tracker.py      # MLflow tracking with graceful fallback
│   │   ├── routers/
│   │   │   ├── pipeline.py     # POST /pipeline/run, GET /pipeline/status
│   │   │   ├── signals.py      # GET/POST/DELETE /signals
│   │   │   └── experiments.py  # GET /experiments
│   │   └── utils/
│   │       └── helpers.py      # Text cleaning
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/client.js       # Axios client, all API calls
│   │   ├── components/
│   │   │   ├── SignalCard.jsx       # Market flags, badges, confidence bar
│   │   │   ├── SignalFeed.jsx       # Signal list with loading state
│   │   │   ├── MarketFilter.jsx     # Market/category filter controls
│   │   │   ├── PipelineControls.jsx # Run pipeline button + status
│   │   │   └── ExperimentLog.jsx    # MLflow run history table
│   │   └── pages/
│   │       ├── Dashboard.jsx   # Main view
│   │       └── Experiments.jsx # MLflow experiments view
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml          # backend + mlflow + frontend
└── supabase_schema.sql         # signals + pipeline_runs table definitions
```

---

## Local Setup (Full Stack with MLflow)

### Prerequisites
- Docker and Docker Compose
- A [Supabase](https://supabase.com) project
- An [OpenRouter](https://openrouter.ai) API key (routes to Claude)
- A [NewsAPI](https://newsapi.org) key

### 1. Clone the repo

```bash
git clone https://github.com/TheElvace/afrisight.git
cd afrisight
```

### 2. Configure environment variables

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in your keys:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=anthropic/claude-sonnet-4-5
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
NEWS_API_KEY=your_newsapi_key
MLFLOW_TRACKING_URI=http://mlflow:5000
ENVIRONMENT=development
```

> **MLFLOW_TRACKING_URI** points to `http://mlflow:5000` because `mlflow` is the Docker Compose service name — Docker's internal DNS resolves it automatically when containers are on the same network.

### 3. Run the Supabase schema

In your Supabase project, go to **SQL Editor** and run the contents of `supabase_schema.sql`. This creates the `signals` and `pipeline_runs` tables.

Then enable Row Level Security policies that allow the backend to read and write. In the SQL Editor run:

```sql
-- signals
create policy "allow all" on signals for all using (true) with check (true);
-- pipeline_runs
create policy "allow all" on pipeline_runs for all using (true) with check (true);
```

### 4. Start all services

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8888 |
| MLflow UI | http://localhost:5000 |
| Frontend | http://localhost:5173 |

### 5. Run the pipeline

Open [http://localhost:5173](http://localhost:5173), click **Run Pipeline**, and watch signals populate. Then open the MLflow UI at [http://localhost:5000](http://localhost:5000) to see the experiment run logged with all parameters and metrics.

---

## Running Without Docker

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` in a `.env` file inside the `frontend/` directory, or the frontend defaults to `http://localhost:8888`.

---

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check, returns `{"status": "ok"}` |
| GET | `/signals` | List signals. Filters: `market`, `category`, `sentiment`, `limit` |
| GET | `/signals/{id}` | Get a single signal by ID |
| POST | `/signals` | Create a signal manually |
| DELETE | `/signals/{id}` | Delete a signal by ID |
| POST | `/pipeline/run` | Trigger full ingestion + classification pipeline |
| GET | `/pipeline/status` | Last pipeline run status and total signal count |
| GET | `/experiments` | List MLflow experiment runs |

**Signal filter example:**
```
GET /signals?market=ng&category=regulatory&limit=20
```

**Supported market values:** `ng`, `ke`, `tz`, `cd`, `et`, `pan-african`, `unknown`

**Supported category values:** `regulatory`, `funding`, `product_launch`, `macro_risk`, `payments`, `other`

**Supported sentiment values:** `positive`, `negative`, `neutral`

---

## Deployment

### Backend — Render

1. Push the repo to GitHub.
2. Create a new **Web Service** on [Render](https://render.com), connect the repo, and set the root directory to `backend/`.
3. Render will auto-detect the `Dockerfile`.
4. Add all environment variables from `.env.example` in the Render dashboard. Set `MLFLOW_TRACKING_URI` to `http://localhost:5000` (MLflow is not available on Render — the tracker will detect this and skip gracefully).
5. Set `ENVIRONMENT=production`.

> **Note on memory:** The sentence-transformer classifier is excluded from the production pipeline because the model alone exceeds Render's free-tier memory limit (512MB). MLflow tracking is also skipped gracefully when unavailable. The LLM pipeline runs fully in production without either dependency.

### Frontend — Vercel

1. Import the repo into [Vercel](https://vercel.com), set the root directory to `frontend/`.
2. Add the environment variable `VITE_API_URL` pointing to your Render backend URL (e.g., `https://afrisight.onrender.com`).
3. Vercel auto-detects Vite. Deploy.

---

## Database Schema

```sql
create table signals (
  id               uuid default gen_random_uuid() primary key,
  created_at       timestamptz default now(),
  title            text not null,
  source_url       text,
  market           text default 'unknown',
  category         text default 'other',
  sentiment        text default 'neutral',
  summary          text not null,
  confidence_score float default 0.0,
  raw_text         text,
  run_id           text
);

create table pipeline_runs (
  id               uuid default gen_random_uuid() primary key,
  created_at       timestamptz default now(),
  run_id           text not null,
  article_count    int default 0,
  signal_count     int default 0,
  avg_confidence   float default 0.0,
  duration_seconds float default 0.0,
  mlflow_run_id    text,
  status           text default 'completed'
);
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | API key from [openrouter.ai](https://openrouter.ai) |
| `OPENROUTER_MODEL` | Model to use (e.g. `anthropic/claude-sonnet-4-5`) |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_KEY` | Your Supabase anon/public key |
| `NEWS_API_KEY` | API key from [newsapi.org](https://newsapi.org) |
| `MLFLOW_TRACKING_URI` | `http://mlflow:5000` locally, `http://localhost:5000` on Render (will gracefully skip) |
| `ENVIRONMENT` | `development` or `production` |

---

## Key Build Decisions

**Why OpenRouter instead of Anthropic directly?**
OpenRouter provides an OpenAI-compatible API endpoint, which means `langchain-openai`'s `ChatOpenAI` class works without any custom integration. It also allows swapping models (GPT-4o, Gemini, Mistral) by changing a single environment variable.

**Why remove the sentence-transformer classifier from production?**
The `all-MiniLM-L6-v2` model requires loading ~90MB of weights into memory at startup. On Render's free tier (512MB total), this caused the server to crash before it could accept any requests. The LLM already handles classification with high fidelity, so the embedding classifier serves a different purpose locally: it allows you to see how vector similarity compares to LLM classification as an experiment.

**Why does MLflow fallback to a UUID?**
`start_pipeline_run` returns either a real MLflow run ID or a `uuid4()` string. The rest of the pipeline uses this as an opaque identifier — it gets stored in the database regardless. This means the pipeline run is always recorded in Supabase even when MLflow isn't running, and the API surface stays consistent.

---

## License

MIT
