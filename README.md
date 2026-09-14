# SE Attack Modeling

A web platform for **attack modeling and automated web-application security
scanning**. Built as my bachelor's thesis project — it crawls a target site,
builds a site map, and runs a suite of vulnerability analyzers, then renders a
human-readable report with CWE references.

## Features

- **Crawler + site map** — walks the target site, collects endpoints and HTML
  forms, builds a graph of the attack surface.
- **Vulnerability analyzers**, each pluggable behind a common `BaseAnalyzer`
  interface:
  - `SQLiAnalyzer` — SQL injection
  - `XSSAnalyzer` — cross-site scripting
  - `CSRFAnalyzer` — CSRF
  - `BruteforceAnalyzer` — login brute-force detection
  - `ConfigAnalyzer` — security misconfiguration / static analysis
- **Async scan engine** — concurrent scanning with configurable depth and
  concurrency, persisted scan state and statuses.
- **CWE database** — bundled CWE reference data (seeded via Alembic migration)
  so each finding links to a standard weakness ID.
- **Reports** — HTML output with RU/EN localization (`Accept-Language`).
- **REST API** — JWT auth, users, scans, and CWE lookup endpoints.
- **Web UI** — React + Vite + TypeScript frontend served behind Nginx.

## Stack

| Layer     | Tech |
|-----------|------|
| Backend   | Python, FastAPI, SQLAlchemy (async + sync), Alembic, aiohttp, Selenium |
| Database  | PostgreSQL 14 |
| Frontend  | React, TypeScript, Vite |
| Infra     | Docker Compose, Nginx |

## Architecture

```
                    ┌──────────────┐
        HTTP        │   frontend   │  React + Vite (port 80)
   ───────────────► │   (Nginx)    │
                    └──────┬───────┘
                           │ REST / JSON
                    ┌──────▼───────┐
                    │   backend    │  FastAPI (port 8000)
                    │  ┌─────────┐ │
                    │  │ crawler │ │  builds SiteMap
                    │  └────┬────┘ │
                    │  ┌────▼────┐ │
                    │  │  engine │ │  async ScanEngine
                    │  └────┬────┘ │
                    │  ┌────▼─────────────┐ │
                    │  │    analyzers     │ │  SQLi / XSS / CSRF /
                    │  │                  │ │  Bruteforce / Config
                    │  └────┬─────────────┘ │
                    └───────┼───────────────┘
                            │ SQLAlchemy
                    ┌───────▼───────────────┐
                    │   PostgreSQL 14       │  scans, vulns, CWE
                    └───────────────────────┘
```

## Run

```bash
docker compose up --build
```

- Frontend: http://localhost
- API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Structure

```
app/
  core/            scan engine, analyzers, reports, scanner (crawler/mapper)
  routers/         auth, users, scans, cwe
  models/          SQLAlchemy models (user, scan, vulnerability, cwe)
  services/        scanner orchestration (sast, fake scanner)
  alembic/         DB migrations (incl. CWE data seed)
frontend/          React + Vite + TS UI
docs/              thesis-related PDFs (specification, requirements)
```

## Notes

- This is a research/educational project; the analyzers are signature- and
  heuristic-based and are not a substitute for a production-grade scanner
  (Burp, ZAP, Nuclei).
- Configuration is environment-driven: DB creds, `SECRET_KEY`, API key and CORS
  origins come from `.env` (see `.env.example`). No real secrets live in the code.

## Tests

```bash
cd app
python -m venv .venv && source .venv/bin/activate
pip install pytest sqlalchemy aiohttp python-dotenv greenlet bcrypt python-jose
python -m pytest tests/
```

Covers analyzer detection logic (SQLi error/time-based, XSS reflection) and
config hygiene (no hardcoded secrets).

## Roadmap

- [x] Move DB credentials and `SECRET_KEY` out of `config.py` into environment
      variables / `.env`.
- [ ] Per-analyzer severity tuning and confidence scoring.
- [ ] Rate limiting and scan scheduling.
