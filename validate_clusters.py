"""Validate app-relevant cluster 4 and 7 values directly from the H5AD file."""
from pathlib import Path

import scanpy as sc

DATA_PATH = Path(__file__).parent / "data" / "pbmc3k.h5ad"
CLUSTERS = ("4", "7")


def main() -> None:
    adata = sc.read_h5ad(DATA_PATH)
    clusters = adata.obs["leiden"].astype(str)
    print(f"Dataset: {DATA_PATH}")
    print(f"Cell count: {adata.n_obs}")
    print(f"Gene count: {adata.n_vars}")

    sc.tl.rank_genes_groups(
        adata,
        "leiden",
        groups=list(CLUSTERS),
        reference="rest",
        method="wilcoxon",
        n_genes=5,
        use_raw=False,
        key_added="validation_markers",
    )
    ranked = adata.uns["validation_markers"]

    for cluster in CLUSTERS:
        cells = clusters == cluster
        names = [str(name) for name in ranked["names"][cluster][:5]]
        print(f"\nCluster {cluster}")
        print(f"  Cell count: {int(cells.sum())}")
        print(
            "  Detected genes/cell: "
            f"median={adata.obs.loc[cells, 'n_genes'].median():.1f}, "
            f"range={int(adata.obs.loc[cells, 'n_genes'].min())}-"
            f"{int(adata.obs.loc[cells, 'n_genes'].max())}"
        )
        print(
            "  Mitochondrial percentage: "
            f"median={adata.obs.loc[cells, 'pct_mito'].median():.2f}%, "
            f"range={adata.obs.loc[cells, 'pct_mito'].min():.2f}-"
            f"{adata.obs.loc[cells, 'pct_mito'].max():.2f}%"
        )
        print(f"  Top 5 markers: {', '.join(names)}")


if __name__ == "__main__":
    main()
