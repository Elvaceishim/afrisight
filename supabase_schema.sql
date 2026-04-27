create table signals (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  title text not null,
  source_url text,
  market text default 'unknown',
  category text default 'other',
  sentiment text default 'neutral',
  summary text not null,
  confidence_score float default 0.0,
  raw_text text,
  run_id text
);

create table pipeline_runs (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  run_id text not null,
  article_count int default 0,
  signal_count int default 0,
  avg_confidence float default 0.0,
  duration_seconds float default 0.0,
  mlflow_run_id text,
  status text default 'completed'
);
