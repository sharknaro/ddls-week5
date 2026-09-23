# PBMC Single-Cell Explorer

A FastAPI app that loads `data/pbmc3k.h5ad` once during startup and serves a mobile-first Tailwind/Plotly interface.

## Run

```bash
uv venv
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000>.

The API provides:

- `GET /api/umap` — UMAP coordinates, cluster, and QC fields for every cell
- `GET /api/genes/{gene}` — per-cell expression from `adata.X` (log-normalized)
- `GET /api/clusters/{cluster}/markers?n_genes=15` — ranked markers and cluster QC

To use another H5AD, replace `data/pbmc3k.h5ad` or update `DATA_PATH` in `app.py`.
