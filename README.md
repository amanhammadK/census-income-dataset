# Census Income Dataset

A ready-to-query dataset server for **Adult census income records**. Records are shipped as JSON in `data/dataset.json` and exposed through a Model Context Protocol server with `query`, `get_record`, and `get_stats` tools.

## Why this exists

Datasets are only useful when something can query them. This repo bundles a small but real sample dataset with a typed query engine so an MCP client can filter, fetch, and summarize records without standing up a database.

## Data shape

Fields: age, workclass, education, occupation, hours_per_week, income_gt_50k

## Install

```bash
npm install
```

## Run

```bash
npm run build
npm start
```

SSE endpoint: `http://localhost:8080/sse`.

## Regenerate data

```bash
pip install -r requirements.txt
python scripts/generate.py
```

## Tools

| Tool | Purpose |
|------|---------|
| `query_dataset` | Filter records by field equality, with pagination |
| `get_record` | Fetch a single record by id |
| `get_stats` | Numeric min/max/mean per field |

## Test

```bash
npm test
```
