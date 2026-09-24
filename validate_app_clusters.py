"""Print validation values for the app's key small clusters.

Run with: uv run python validate_app_clusters.py
"""
from pathlib import Path

import scanpy as sc

DATA_PATH = Path(__file__).parent / "data" / "pbmc3k.h5ad"

adata = sc.read_h5ad(DATA_PATH)
sc.tl.rank_genes_groups(
    adata,
    "leiden",
    groups=["4", "7"],
    reference="rest",
    method="wilcoxon",
    n_genes=5,
    use_raw=False,
    key_added="validation_markers",
)
ranked = adata.uns["validation_markers"]
clusters = adata.obs["leiden"].astype(str)

print(f"Cells in dataset: {adata.n_obs}")
for cluster in ("4", "7"):
    mask = clusters == cluster
    print(f"\nCluster {cluster}")
    print(f"Cell count: {int(mask.sum())}")
    print(f"Median detected genes/cell: {adata.obs.loc[mask, 'n_genes'].median():.2f}")
    print(f"Median mitochondrial percentage: {adata.obs.loc[mask, 'pct_mito'].median():.2f}%")
    print("Top 5 marker genes: " + ", ".join(str(g) for g in ranked["names"][cluster][:5]))
