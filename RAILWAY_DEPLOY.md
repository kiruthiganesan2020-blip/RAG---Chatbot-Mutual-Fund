# Railway Deployment

This repo is configured to deploy as one Railway web service.

## Deploy

1. Push this repository to GitHub.
2. In Railway, create a new project from the GitHub repo.
3. Keep the root directory as `/`.
4. Railway will read `railway.toml` and use:
   - Builder: Railpack
   - Build command: `pip install -r requirements-railway.txt`
   - Start command: `python simple_backend.py`
   - Health check: `/api/health`
5. Generate a public Railway domain for the service.

The FastAPI backend serves the frontend at `/` and the API at `/api/*`, so no separate frontend service or API URL variable is needed.

## Required Variables

The current deployed backend uses mock responses and does not require API keys.

If you switch to the full RAG backend later, add the keys from `.env.example` in Railway's Variables tab instead of committing `.env`.

## Render

This repo also includes `render.yaml` for Render. It deploys the same single FastAPI service:

- Build command: `pip install -r requirements-railway.txt`
- Start command: `python simple_backend.py`
- Health check: `/api/health`
- Python version: `3.11.9`
