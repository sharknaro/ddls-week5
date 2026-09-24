# PBMC Single-Cell Explorer

A small FastAPI application for exploring the supplied PBMC single-cell dataset in a browser. The app loads `data/pbmc3k.h5ad` at startup and provides a UMAP, cluster QC summaries, marker tables, and gene-expression coloring.

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)

The project uses `uv` for its virtual environment and dependency management. Dependencies include Scanpy, FastAPI, and Uvicorn. The browser UI loads Tailwind CSS and Plotly.js from CDN script tags; there is no npm dependency or frontend build step.

## Setup and run

From the project directory:

```bash
uv venv
uv sync
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000>.

The app expects the dataset at `data/pbmc3k.h5ad`. To use another H5AD file, replace that file or update `DATA_PATH` in `app.py`.

## Browser features

- UMAP colored by:
  - Cluster
  - Detected genes per cell
  - Mitochondrial reads (%)
  - Gene expression
- Scroll-wheel/touchpad zoom on the UMAP
- Pan tool in the left sidebar
- Autoscale and image download tools
- Gene selector with loading and not-found feedback
- Quick selection of clusters 4 and 7
- Selected-cluster QC and detailed marker table
- Full cluster overview for clusters 0–7 with cell counts, QC medians, and top markers
- Cream/beige light theme with dark, readable tables

The Plotly default modebar is hidden. Plot controls are provided in the left sidebar.

## API endpoints

- `GET /api/umap` — UMAP coordinates, cluster labels, and per-cell QC fields
- `GET /api/genes/{gene}` — per-cell log-normalized expression from `adata.X`
- `GET /api/clusters/overview` — all-cluster counts, QC medians, and five top markers
- `GET /api/clusters/{cluster}/markers?n_genes=15` — ranked markers and selected-cluster QC

## Reproducible validation

Validate the key cluster 4 and 7 values with:

```bash
uv run python validate_app_clusters.py
```

The script reports the dataset cell count, cluster cell counts, QC medians, and top five markers.

Run the seeded sampled trap checks with:

```bash
uv run python sampled_trap_check.py
```

This samples up to 30 cells per cluster with seed 42, compares sample and full-cluster QC, checks marker coherence and raw-count incompatible-lineage co-expression, and writes the detailed report to `results/sampled_trap_check.csv`. `PASS` means no obvious artifact was detected; it does not confirm a novel cell type.

## Data provenance and scope

The supplied H5AD contains 2,700 cells, precomputed clusters, UMAP coordinates, QC metadata, log-normalized `adata.X`, and raw counts in `adata.layers["counts"]`. Donor/batch identifiers and formal doublet scores are not available in the supplied data, so donor-level reproducibility and formal doublet-score validation are out of scope.
