from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import numpy as np
import scanpy as sc
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

DATA_PATH = Path(__file__).parent / "data" / "pbmc3k.h5ad"
STATE: dict[str, Any] = {}


def _as_float(value: Any) -> float:
    return float(value) if np.isfinite(value) else 0.0


def _matrix_column(adata, gene: str) -> np.ndarray:
    matches = {str(name).upper(): str(name) for name in adata.var_names}
    actual_gene = matches.get(gene.upper())
    if actual_gene is None:
        raise HTTPException(status_code=404, detail=f"Gene not found: {gene}")
    values = adata[:, actual_gene].X
    if hasattr(values, "toarray"):
        values = values.toarray()
    return np.asarray(values).ravel()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not DATA_PATH.exists():
        raise RuntimeError(f"H5AD file not found: {DATA_PATH}")
    adata = sc.read_h5ad(DATA_PATH)
    if "X_umap" not in adata.obsm:
        raise RuntimeError("The H5AD file does not contain obsm['X_umap']")
    STATE["adata"] = adata
    yield
    STATE.clear()


app = FastAPI(title="PBMC Single-Cell Explorer", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return HTML_PAGE


@app.get("/api/umap")
async def umap() -> dict[str, Any]:
    adata = STATE["adata"]
    coords = np.asarray(adata.obsm["X_umap"])
    clusters = adata.obs["leiden"].astype(str).to_numpy()
    return {
        "cells": [
            {
                "cell_id": str(cell_id),
                "x": _as_float(point[0]),
                "y": _as_float(point[1]),
                "cluster": cluster,
                "n_genes": int(n_genes),
                "pct_mito": _as_float(pct_mito),
            }
            for cell_id, point, cluster, n_genes, pct_mito in zip(
                adata.obs_names,
                coords,
                clusters,
                adata.obs["n_genes"],
                adata.obs["pct_mito"],
            )
        ]
    }


@app.get("/api/genes/{gene}")
async def gene_expression(gene: str) -> dict[str, Any]:
    adata = STATE["adata"]
    values = _matrix_column(adata, gene)
    return {
        "gene": gene,
        "layer": "adata.X (log-normalized expression)",
        "values": [
            {"cell_id": str(cell_id), "cluster": str(cluster), "expression": _as_float(value)}
            for cell_id, cluster, value in zip(adata.obs_names, adata.obs["leiden"], values)
        ],
    }


@app.get("/api/clusters/overview")
async def clusters_overview() -> dict[str, Any]:
    adata = STATE["adata"]
    sc.tl.rank_genes_groups(
        adata, "leiden", reference="rest", method="wilcoxon",
        n_genes=5, use_raw=False, key_added="api_overview_markers",
    )
    ranked = adata.uns["api_overview_markers"]
    cluster_values = adata.obs["leiden"].astype(str)
    clusters = [str(i) for i in range(8)]
    return {"clusters": [
        {
            "cluster": cluster,
            "cell_count": int((cluster_values == cluster).sum()),
            "median_detected_genes": _as_float(adata.obs.loc[cluster_values == cluster, "n_genes"].median()),
            "median_mitochondrial_percent": _as_float(adata.obs.loc[cluster_values == cluster, "pct_mito"].median()),
            "top_markers": [str(gene) for gene in ranked["names"][cluster][:5]],
        }
        for cluster in clusters
    ]}


@app.get("/api/clusters/{cluster}/markers")
async def cluster_markers(
    cluster: str,
    n_genes: int = Query(default=15, ge=1, le=100),
) -> dict[str, Any]:
    adata = STATE["adata"]
    if cluster not in adata.obs["leiden"].astype(str).unique():
        raise HTTPException(status_code=404, detail=f"Unknown cluster: {cluster}")
    sc.tl.rank_genes_groups(
        adata, "leiden", groups=[cluster], reference="rest", method="wilcoxon",
        n_genes=n_genes, use_raw=False, key_added="api_markers",
    )
    ranked = adata.uns["api_markers"]
    names = ranked["names"][cluster]
    markers = []
    for i, name in enumerate(names):
        markers.append({
            "gene": str(name),
            "score": _as_float(ranked["scores"][cluster][i]),
            "logfoldchange": _as_float(ranked["logfoldchanges"][cluster][i]),
            "pval_adj": _as_float(ranked["pvals_adj"][cluster][i]),
        })
    cells = adata.obs["leiden"].astype(str) == cluster
    return {
        "cluster": cluster,
        "n_cells": int(cells.sum()),
        "quality": {
            "n_genes_median": _as_float(adata.obs.loc[cells, "n_genes"].median()),
            "n_genes_range": [int(adata.obs.loc[cells, "n_genes"].min()), int(adata.obs.loc[cells, "n_genes"].max())],
            "pct_mito_median": _as_float(adata.obs.loc[cells, "pct_mito"].median()),
            "pct_mito_range": [_as_float(adata.obs.loc[cells, "pct_mito"].min()), _as_float(adata.obs.loc[cells, "pct_mito"].max())],
        },
        "markers": markers,
    }


HTML_PAGE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <style>
    .plot-tool { width: 2rem; height: 2rem; border: 1px solid #cbbda9; border-radius: .375rem; background: #fffaf1; color: #334155; font-weight: 700; line-height: 1; }
    .plot-tool:hover, .plot-tool:focus-visible { background: #e8dccb; color: #111827; outline: none; }
    .plot-tool.active { background: #6f3f24; border-color: #6f3f24; color: #fffaf1; }
  </style>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PBMC Single-Cell Explorer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>
<body class="min-h-screen bg-[#f4efe6] text-slate-900">
  <main class="mx-auto max-w-7xl p-4 sm:p-6">
    <header class="mb-5">
      <p class="text-sm font-semibold uppercase tracking-widest text-[#6f3f24]">PBMC single-cell explorer</p>
      <h1 class="mt-1 text-3xl font-bold tracking-tight">UMAP and cluster markers</h1>
      <p class="mt-2 max-w-3xl text-slate-600">Explore 2,700 cells from <code>pbmc3k.h5ad</code>. Expression values use log-normalized <code>adata.X</code>.</p>
    </header>
    <section class="grid gap-4 lg:grid-cols-[18rem_1fr]">
      <aside class="h-[62vh] min-h-[28rem] overflow-y-auto rounded-2xl border border-[#d8cdbd] bg-[#fffaf1] p-4 shadow-xl">
        <div class="mb-4"><h2 class="text-sm font-semibold uppercase tracking-widest text-[#6f3f24]">Plot tools</h2><div id="plotToolbar" class="mt-2 flex flex-wrap gap-1" role="toolbar" aria-label="Plot controls"><button data-action="pan" title="Pan" aria-label="Pan" class="plot-tool">↔</button><button data-action="autoscale" title="Autoscale" aria-label="Autoscale" class="plot-tool">⤢</button><button data-action="download" title="Download plot image" aria-label="Download plot image" class="plot-tool">⇩</button></div></div>
        <div class="space-y-4">
          <label class="block"><span class="text-sm font-medium text-slate-700">Color UMAP by</span>
            <select id="colorBy" class="mt-1 w-full rounded-lg border border-[#cbbda9] bg-white px-3 py-2 text-slate-900"><option value="cluster">Cluster</option><option value="n_genes">Detected genes per cell</option><option value="pct_mito">Mitochondrial reads (%)</option><option value="gene">Gene expression</option></select>
          </label>
          <label id="geneControl" class="hidden block"><span class="text-sm font-medium text-slate-700">Gene expression</span>
            <div class="mt-1 flex gap-2"><select id="gene" class="min-w-0 flex-1 rounded-lg border border-[#cbbda9] bg-white px-3 py-2 text-slate-900" aria-label="Select a gene"><option value="">Choose a gene…</option></select><button id="geneBtn" class="rounded-lg bg-[#b45309] px-3 py-2 font-semibold text-white">Plot gene</button></div>
            <p class="mt-1 text-xs text-slate-600">Choose a gene to color each UMAP cell by its log-normalized expression.</p>
            <p id="geneStatus" class="mt-1 text-xs text-slate-600"></p>
          </label>
          <div><span class="text-sm text-slate-700">Quick-select clusters</span><div class="mt-1 flex gap-2"><button class="quick rounded-lg border border-slate-700 px-3 py-1 text-sm" data-cluster="4">Cluster 4</button><button class="quick rounded-lg border border-slate-700 px-3 py-1 text-sm" data-cluster="7">Cluster 7</button></div></div>
          <label class="block"><span class="text-sm text-slate-700">Selected cluster</span>
            <select id="cluster" class="mt-1 w-full rounded-lg border border-[#cbbda9] bg-white px-3 py-2 text-slate-900"></select>
          </label>
          <div id="quality" class="rounded-lg bg-[#eee5d6] p-3 text-sm text-slate-700">Loading selected-cluster QC…</div>
        </div>
      </aside>
      <section class="min-w-0">
        <div class="relative h-[62vh] min-h-[28rem] rounded-2xl border border-[#d8cdbd] bg-[#fffaf1]"><div id="plot" class="h-full w-full"></div></div>
      </section>
      <section class="col-span-full min-w-0 space-y-4">
        <div class="overflow-hidden rounded-2xl border border-[#d8cdbd] bg-[#fffaf1] text-slate-800">
          <div class="border-b border-[#e5dacb] px-4 py-3"><h2 class="font-semibold">Top markers</h2></div>
          <div class="overflow-x-auto bg-[#fffaf1]"><table class="w-full text-left text-sm text-slate-800"><thead class="bg-[#e8dccb] text-slate-900"><tr><th class="px-4 py-2">Gene</th><th class="px-4 py-2">Score</th><th class="px-4 py-2">Log fold change</th><th class="px-4 py-2">Adjusted p-value</th></tr></thead><tbody id="markers"></tbody></table></div>
        </div>
        <div class="overflow-hidden rounded-2xl border border-[#d8cdbd] bg-[#fffaf1] text-slate-800">
          <div class="border-b border-[#e5dacb] px-4 py-3"><h2 class="font-semibold">All-cluster overview</h2><p class="text-xs text-slate-500">Every cluster, its size, QC medians, and five highest-ranked markers.</p></div>
          <div class="overflow-x-auto bg-[#fffaf1]"><table class="w-full text-left text-sm text-slate-800"><thead class="bg-[#e8dccb] text-slate-900"><tr><th class="px-4 py-2">Cluster</th><th class="px-4 py-2">Cell count</th><th class="px-4 py-2">Median detected genes/cell</th><th class="px-4 py-2">Median mitochondrial %</th><th class="px-4 py-2">Top 5 marker genes</th></tr></thead><tbody id="overview"></tbody></table></div>
        </div>
      </section>
    </section>
  </main>
<script>
const palette = ['#22d3ee','#a78bfa','#f472b6','#facc15','#4ade80','#fb923c','#60a5fa','#f87171'];
let umapData;
let activeView = 'cluster';
const $ = id => document.getElementById(id);
async function load() {
  $('plot').innerHTML = '<div class="flex h-full items-center justify-center text-slate-400">Loading UMAP…</div>';
  $('geneStatus').textContent = 'Loading gene suggestions…';
  try {
    const response = await fetch('/api/umap'); if (!response.ok) throw new Error('UMAP request failed');
    umapData = (await response.json()).cells;
    const clusters = [...new Set(umapData.map(d => d.cluster))].sort((a,b) => +a - +b);
    $('cluster').innerHTML = clusters.map(c => `<option value="${c}">Cluster ${c}</option>`).join('');
    const geneOptions = ['FCER1G','LST1','CD3D','FCGR3A','AIF1','CTSS','CD68','CST3','STMN1','PCNA','TYMS'];
    $('gene').innerHTML = '<option value="">Choose a gene…</option>' + geneOptions.map(g => `<option value="${g}">${g}</option>`).join('');
    $('geneStatus').textContent = 'Gene values use log-normalized expression from adata.X.';
    $('geneControl').classList.add('hidden');
    $('colorBy').addEventListener('change', () => { activeView = $('colorBy').value; $('geneControl').classList.toggle('hidden', activeView !== 'gene'); if (activeView !== 'gene') draw(); });
    $('geneBtn').addEventListener('click', plotGene);
    $('cluster').addEventListener('change', loadMarkers);
    document.querySelectorAll('.quick').forEach(button => button.addEventListener('click', () => { $('cluster').value = button.dataset.cluster; loadMarkers(); }));
    await loadOverview(); draw(); await loadMarkers();
  } catch (error) { $('plot').innerHTML = `<div class="flex h-full items-center justify-center p-6 text-center text-red-300">Could not load the UMAP. ${error.message}</div>`; }
}
async function loadOverview() {
  const data = await (await fetch('/api/clusters/overview')).json();
  $('overview').innerHTML = data.clusters.map(d => `<tr class="border-t border-[#e5dacb] bg-[#fffaf1] text-slate-800"><td class="px-4 py-2 font-medium">Cluster ${d.cluster}</td><td class="px-4 py-2">${d.cell_count}</td><td class="px-4 py-2">${d.median_detected_genes.toFixed(0)}</td><td class="px-4 py-2">${d.median_mitochondrial_percent.toFixed(2)}%</td><td class="px-4 py-2">${d.top_markers.join(', ')}</td></tr>`).join('');
}
function draw() {
  const mode = activeView;
  $('colorBy').value = mode === 'gene' ? 'gene' : mode;
  $('geneControl').classList.toggle('hidden', mode !== 'gene');
  const labels = {cluster:'Cluster', n_genes:'Gene count<br>per cell', pct_mito:'Mitochondrial<br>reads (%)', gene:'Gene expression'};
  if (mode === 'cluster') {
    const traces = [...new Set(umapData.map(d => d.cluster))].sort((a,b)=>+a-+b).map((c,i) => { const z=umapData.filter(d=>d.cluster===c); return {x:z.map(d=>d.x),y:z.map(d=>d.y),mode:'markers',type:'scattergl',name:`Cluster ${c}`,text:z.map(d=>`${d.cell_id}<br>Detected genes: ${d.n_genes}<br>Mitochondrial percentage: ${d.pct_mito.toFixed(2)}%`),hoverinfo:'text',marker:{color:palette[i%palette.length],size:6,opacity:.8}}; }); Plotly.newPlot('plot',traces,layout('UMAP — coloured by Cluster'),{responsive:true,displaylogo:false,displayModeBar:false,scrollZoom:true});
  } else { const vals=umapData.map(d=>d[mode]); Plotly.newPlot('plot',[{x:umapData.map(d=>d.x),y:umapData.map(d=>d.y),mode:'markers',type:'scattergl',text:umapData.map(d=>d.cell_id),hoverinfo:'text',marker:{color:vals,colorscale:'Viridis',size:6,colorbar:{title:{text:labels[mode],side:'top'},titlefont:{size:12},tickfont:{size:10}}}}],layout(`UMAP — coloured by ${labels[mode]}`),{responsive:true,displaylogo:false,displayModeBar:false,scrollZoom:true}); }
}
function layout(title) { return {title:{text:title,font:{color:'#1f2937'}},paper_bgcolor:'#fffaf1',plot_bgcolor:'#fffaf1',font:{color:'#475569'},margin:{l:55,r:95,t:55,b:60},xaxis:{title:'UMAP 1',gridcolor:'#e5dacb'},yaxis:{title:'UMAP 2',gridcolor:'#e5dacb'},legend:{bgcolor:'#fffaf1',font:{color:'#334155'},orientation:'v',x:1.02,xanchor:'left',y:1,yanchor:'top'}}; }
async function plotGene() { const gene=$('gene').value.trim(); if(!gene)return; $('geneStatus').textContent = `Loading ${gene} expression…`; const r=await fetch(`/api/genes/${encodeURIComponent(gene)}`); if(!r.ok){$('geneStatus').textContent = `Gene not found: ${gene}`; return;} const data=await r.json(); const values=data.values; const byId=new Map(values.map(d=>[d.cell_id,d.expression])); activeView = 'gene'; $('colorBy').value = 'gene'; $('geneControl').classList.remove('hidden'); $('geneStatus').textContent = `Active colouring: ${data.gene} expression (log-normalized adata.X).`; Plotly.newPlot('plot',[{x:umapData.map(d=>d.x),y:umapData.map(d=>d.y),mode:'markers',type:'scattergl',text:umapData.map(d=>d.cell_id),hoverinfo:'text',marker:{color:umapData.map(d=>byId.get(d.cell_id)),colorscale:'Viridis',size:6,colorbar:{title:{text:`${data.gene}<br>expression`,side:'top'},titlefont:{size:12},tickfont:{size:10}}}}],layout(`UMAP — coloured by Gene expression (${data.gene})`),{responsive:true,displaylogo:false,displayModeBar:false,scrollZoom:true}); }
async function loadMarkers() { const c=$('cluster').value; if(c===undefined)return; $('quality').textContent = `Loading Cluster ${c} QC…`; const d=await (await fetch(`/api/clusters/${c}/markers?n_genes=15`)).json(); $('quality').innerHTML=`<b>Cluster ${c}</b><br>Cell count: ${d.n_cells}<br>Median detected genes/cell: ${d.quality.n_genes_median.toFixed(0)} (range ${d.quality.n_genes_range.join('–')})<br>Median mitochondrial percentage: ${d.quality.pct_mito_median.toFixed(2)}% (range ${d.quality.pct_mito_range.map(x=>x.toFixed(2)).join('–')}%)`; $('markers').innerHTML=d.markers.map(m=>`<tr class="border-t border-[#e5dacb] bg-[#fffaf1] text-slate-800"><td class="px-4 py-2 font-medium">${m.gene}</td><td class="px-4 py-2">${m.score.toFixed(2)}</td><td class="px-4 py-2">${m.logfoldchange.toFixed(2)}</td><td class="px-4 py-2">${m.pval_adj.toExponential(2)}</td></tr>`).join(''); }
function wirePlotToolbar() {
  document.querySelectorAll('#plotToolbar [data-action]').forEach(button => button.addEventListener('click', () => {
    const action = button.dataset.action;
    const plot = $('plot');
    if (action === 'pan') {
      const isActive = button.classList.contains('active');
      button.classList.toggle('active', !isActive);
      Plotly.relayout(plot, {'dragmode': isActive ? 'zoom' : 'pan'});
    }
    if (action === 'autoscale') Plotly.relayout(plot, {'xaxis.autorange': true, 'yaxis.autorange': true});
    if (action === 'download') Plotly.downloadImage(plot, {format:'png', filename:'pbmc-umap', height:900, width:1400});
  }));
}
wirePlotToolbar();
load();
</script>
</body></html>'''
