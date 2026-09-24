"""Seeded per-cluster trap checks for the supplied PBMC AnnData file.

Run with: uv run python sampled_trap_check.py
The compact report is written to results/sampled_trap_check.csv.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc

DATA_PATH = Path(__file__).parent / "data" / "pbmc3k.h5ad"
RESULTS_PATH = Path(__file__).parent / "results" / "sampled_trap_check.csv"
SEED = 42
MAX_SAMPLE = 30

# Marker panels are deliberately explicit and conservative: they support trap checks,
# not a novel-cell-type claim. Housekeeping/cell-cycle genes are tracked separately.
LINEAGE_MARKERS = {
    "T/NK": {"CD3D", "CD3E", "TRBC1", "TRBC2", "IL7R", "NKG7", "GNLY", "CCL5"},
    "B": {"MS4A1", "CD79A", "CD37", "CD74", "HLA-DRA", "CD79B", "CD83"},
    "myeloid": {"LYZ", "LST1", "FCER1G", "CTSS", "AIF1", "FCGR3A", "LGALS3", "TYROBP", "S100A8", "S100A9"},
    "platelet": {"PPBP", "PF4", "GNG11", "RGS18"},
    "dendritic": {"FCER1A", "CLEC10A", "CD1C", "HLA-DPA1"},
}
HOUSEKEEPING = {"MALAT1", "RPLP0", "RPL3", "RPL13", "RPS3", "RPS6", "RPS12", "RPS18", "RPS27", "RPL10", "RPL32", "GAPDH", "ACTB", "B2M"}
CELL_CYCLE = {"MKI67", "TOP2A", "STMN1", "PCNA", "TYMS", "TUBA1B", "HMGB2", "HIST1H4C", "KIAA0101"}


def fmt_range(values: pd.Series, decimals: int = 0) -> str:
    return f"{values.min():.{decimals}f}–{values.max():.{decimals}f}"


def gene_names(names) -> list[str]:
    return [str(name).upper() for name in names]


def main() -> None:
    adata = sc.read_h5ad(DATA_PATH)
    if "counts" not in adata.layers:
        raise RuntimeError('Expected raw counts in adata.layers["counts"]')
    if not {"n_genes", "pct_mito", "leiden"}.issubset(adata.obs):
        raise RuntimeError("Expected n_genes, pct_mito, and leiden in adata.obs")

    clusters = adata.obs["leiden"].astype(str)
    rng = np.random.default_rng(SEED)
    rows = []

    sc.tl.rank_genes_groups(
        adata, "leiden", reference="rest", method="wilcoxon",
        n_genes=10, use_raw=False, key_added="sampled_trap_markers",
    )
    ranked = adata.uns["sampled_trap_markers"]["names"]

    for cluster in sorted(clusters.unique(), key=int):
        all_idx = np.flatnonzero(clusters.to_numpy() == cluster)
        sample_idx = rng.choice(all_idx, size=min(MAX_SAMPLE, len(all_idx)), replace=False)
        sample_idx.sort()
        sampled = adata.obs.iloc[sample_idx]
        full = adata.obs.iloc[all_idx]

        top = gene_names(ranked[cluster][:10])
        lineage_hits = {name: sorted(set(top) & markers) for name, markers in LINEAGE_MARKERS.items()}
        coherent_lineages = {name for name, hits in lineage_hits.items() if len(hits) >= 2}
        mixed_lineage = len(coherent_lineages) >= 2
        housekeeping_fraction = len(set(top) & (HOUSEKEEPING | CELL_CYCLE)) / len(top)

        counts = adata.layers["counts"][sample_idx]
        if hasattr(counts, "toarray"):
            counts = counts.toarray()
        counts = np.asarray(counts)
        var_names = [str(v).upper() for v in adata.var_names]
        gene_to_col = {gene: i for i, gene in enumerate(var_names)}
        incompatible_pairs = [("T/NK", "myeloid"), ("T/NK", "B"), ("B", "myeloid"), ("platelet", "myeloid")]
        primary_lineages = sorted(coherent_lineages)
        coexpression_pairs = []
        for left, right in incompatible_pairs:
            left_cols = [gene_to_col[g] for g in LINEAGE_MARKERS[left] if g in gene_to_col]
            right_cols = [gene_to_col[g] for g in LINEAGE_MARKERS[right] if g in gene_to_col]
            if not left_cols or not right_cols:
                continue
            # Require at least two detected markers from each program and a
            # substantial fraction of sampled cells before flagging a cluster.
            left_detected = (counts[:, left_cols] > 0).sum(axis=1) >= 2
            right_detected = (counts[:, right_cols] > 0).sum(axis=1) >= 2
            n_both = int((left_detected & right_detected).sum())
            if n_both >= max(3, int(np.ceil(len(sample_idx) * 0.20))) and left in primary_lineages and right in primary_lineages:
                coexpression_pairs.append(f"{left}+{right}: {n_both}/{len(sample_idx)}")
        high_complexity = int((sampled["n_genes"] > full["n_genes"].quantile(0.95)).sum())
        representative = (
            abs(float(sampled["n_genes"].median()) - float(full["n_genes"].median())) <= max(100, float(full["n_genes"].median()) * 0.15)
            and abs(float(sampled["pct_mito"].median()) - float(full["pct_mito"].median())) <= max(1.0, float(full["pct_mito"].median()) * 0.25)
        )

        status = "PASS"
        warnings = []
        if not representative:
            status = "WARN"
            warnings.append("sample differs from full-cluster QC")
        if mixed_lineage or coexpression_pairs:
            status = "FAIL"
            warnings.append("raw-count incompatible-lineage co-expression")
        elif housekeeping_fraction >= 0.5 or high_complexity >= max(2, len(sample_idx) // 5):
            status = "WARN"
            warnings.append("housekeeping/cell-cycle or high-complexity signal")
        if not coherent_lineages:
            status = "WARN" if status == "PASS" else status
            warnings.append("marker identity not coherent")

        if coherent_lineages:
            interpretation = "coherent " + "/".join(sorted(coherent_lineages)) + " program; not a novelty claim"
        else:
            interpretation = "unclear identity; do not advance novelty claim"
        marker_coherence = ", ".join(f"{name} ({', '.join(hits[:3])})" for name, hits in lineage_hits.items() if hits) or "no panel hits in top 10"
        mixed_evidence = "; ".join(coexpression_pairs) if coexpression_pairs else ("none in sampled raw counts" if not mixed_lineage else "multiple incompatible marker programs")
        rows.append({
            "cluster": cluster,
            "sampled_n": len(sample_idx),
            "median_n_genes": round(float(sampled["n_genes"].median()), 2),
            "range_n_genes": fmt_range(sampled["n_genes"]),
            "median_pct_mito": round(float(sampled["pct_mito"].median()), 2),
            "range_pct_mito": fmt_range(sampled["pct_mito"], 2),
            "marker_coherence": marker_coherence,
            "mixed_lineage_evidence": mixed_evidence,
            "likely_interpretation": interpretation,
            "trap_check_status": status,
            "full_median_n_genes": round(float(full["n_genes"].median()), 2),
            "full_median_pct_mito": round(float(full["pct_mito"].median()), 2),
            "sample_representative_of_full_cluster": "yes" if representative else "no",
            "top_markers": ", ".join(top[:5]),
            "notes": "; ".join(warnings) if warnings else "no obvious artifact detected",
        })

    report = pd.DataFrame(rows)
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(RESULTS_PATH, index=False)
    print(report[["cluster", "sampled_n", "median_n_genes", "range_n_genes", "median_pct_mito", "range_pct_mito", "marker_coherence", "mixed_lineage_evidence", "likely_interpretation", "trap_check_status"]].to_string(index=False))
    print(f"\nSeed: {SEED}; maximum sampled per cluster: {MAX_SAMPLE}")
    print(f"Full-cluster comparison and detailed fields: {RESULTS_PATH}")
    print("PASS means no obvious artifact detected; it does not confirm a novel cell type.")


if __name__ == "__main__":
    main()
