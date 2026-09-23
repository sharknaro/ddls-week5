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
    if gene not in adata.var_names:
        raise HTTPException(status_code=404, detail=f"Unknown gene: {gene}")
    values = adata[:, gene].X
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


@app.get("/api/genes")
async def genes() -> dict[str, Any]:
    adata = STATE["adata"]
    return {"genes": [str(gene) for gene in adata.var_names]}


@app.get("/api/genes/{gene}")
async def gene_expression(gene: str) -> dict[str, Any]:
    adata = STATE["adata"]
    gene = gene.upper()
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
    clusters = sorted(adata.obs["leiden"].astype(str).unique(), key=lambda value: int(value))
    return {
        "clusters": [
            {
                "cluster": cluster,
                "n_cells": int((adata.obs["leiden"].astype(str) == cluster).sum()),
                "median_detected_genes": _as_float(adata.obs.loc[adata.obs["leiden"].astype(str) == cluster, "n_genes"].median()),
                "median_mitochondrial_percentage": _as_float(adata.obs.loc[adata.obs["leiden"].astype(str) == cluster, "pct_mito"].median()),
                "top_markers": [str(gene) for gene in ranked["names"][cluster][:5]],
            }
            for cluster in clusters
        ]
    }


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
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>PBMC Single-Cell Explorer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>
<body class="min-h-screen bg-slate-950 text-slate-100">
  <main class="mx-auto max-w-7xl p-4 sm:p-6">
    <header class="mb-5">
      <p class="text-sm font-semibold uppercase tracking-widest text-cyan-400">PBMC single-cell explorer</p>
      <h1 class="mt-1 text-3xl font-bold tracking-tight">UMAP and cluster markers</h1>
      <p class="mt-2 max-w-3xl text-slate-400">Explore 2,700 cells from <code>pbmc3k.h5ad</code>. Start with the cluster-colored UMAP, then choose a gene and press <b>Show gene</b>.</p>
    </header>
    <section class="grid gap-4 lg:grid-cols-[18rem_1fr]">
      <aside class="rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-xl">
        <div class="mb-4"><h2 class="font-semibold">Controls</h2><p class="text-xs text-slate-500">Choose a view and inspect cells.</p></div>
        <div id="controls" class="space-y-4">
          <label class="block"><span class="text-sm text-slate-300">Color points by</span>
            <select id="colorBy" class="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2"><option value="cluster">Leiden cluster (categorical)</option><option value="n_genes">Detected genes per cell</option><option value="pct_mito">Mitochondrial counts (%)</option></select>
          </label>
          <label class="block"><span class="text-sm text-slate-300">Show a gene on the UMAP</span>
            <div class="mt-1 flex gap-2"><select id="geneSelect" aria-label="Select a gene from the dataset" class="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-800 px-2 py-2"><option>Loading genes…</option></select><button id="geneBtn" class="rounded-lg bg-cyan-500 px-3 py-2 font-semibold text-slate-950">Show gene</button></div>
            <p class="mt-1 text-xs text-slate-500">Select any gene in the dataset to color the UMAP by its log-normalized expression.</p>
          </label>
          <label class="block"><span class="text-sm text-slate-300">Inspect cluster markers</span>
            <select id="cluster" aria-label="Cluster for marker table" class="mt-1 w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2"></select>
          </label>
          <div><span class="text-xs text-slate-500">Quick select</span><div class="mt-1 flex gap-2"><button type="button" data-cluster="4" class="cluster-quick rounded-lg border border-cyan-700 px-3 py-1.5 text-sm text-cyan-200 hover:bg-cyan-950">Cluster 4</button><button type="button" data-cluster="7" class="cluster-quick rounded-lg border border-cyan-700 px-3 py-1.5 text-sm text-cyan-200 hover:bg-cyan-950">Cluster 7</button></div></div>
          <div id="quality" class="rounded-lg bg-slate-800/70 p-3 text-sm text-slate-300">Choose a cluster to see its quality summary and markers.</div>
        </div>
      </aside>
      <section class="min-w-0 space-y-4">
        <div id="status" role="status" aria-live="polite" class="hidden rounded-lg border px-3 py-2 text-sm"></div>
        <div id="activeView" class="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-300">Active coloring: loading…</div>
        <div id="plot" class="h-[62vh] min-h-[28rem] rounded-2xl border border-slate-800 bg-slate-900"><div class="flex h-full items-center justify-center text-slate-400">Loading UMAP…</div></div>
        <div class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
          <div class="border-b border-slate-800 px-4 py-3"><h2 class="font-semibold">Cluster overview</h2><p class="mt-1 text-xs text-slate-500">All clusters, cell counts, and top five markers.</p></div>
          <div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead class="bg-slate-800/70 text-slate-300"><tr><th class="px-4 py-2">Cluster</th><th class="px-4 py-2">Cells</th><th class="px-4 py-2">Median genes/cell</th><th class="px-4 py-2">Median mitochondrial %</th><th class="px-4 py-2">Top 5 markers</th></tr></thead><tbody id="overview"></tbody></table></div>
        </div>
        <div class="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900">
          <div class="border-b border-slate-800 px-4 py-3"><h2 class="font-semibold">Selected cluster markers</h2><p class="mt-1 text-xs text-slate-500">Wilcoxon ranking vs. all other cells; log FC and adjusted p-values.</p></div>
          <div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead class="bg-slate-800/70 text-slate-300"><tr><th class="px-4 py-2">Gene</th><th class="px-4 py-2">Score</th><th class="px-4 py-2">Log FC</th><th class="px-4 py-2">Adjusted p</th></tr></thead><tbody id="markers"></tbody></table></div>
        </div>
      </section>
    </section>
  </main>
<script>
const palette = ['#22d3ee','#a78bfa','#f472b6','#facc15','#4ade80','#fb923c','#60a5fa','#f87171'];
let umapData;
const $ = id => document.getElementById(id);
function setStatus(message, kind = 'info') { const el = $('status'); if (!message) { el.className = 'hidden'; el.textContent = ''; return; } const styles = {info: 'border-cyan-800 bg-cyan-950/50 text-cyan-200', error: 'border-red-800 bg-red-950/50 text-red-200', success: 'border-emerald-800 bg-emerald-950/50 text-emerald-200'}; el.className = `rounded-lg border px-3 py-2 text-sm ${styles[kind] || styles.info}`; el.textContent = message; }
function setBusy(button, busy, label) { button.disabled = busy; button.textContent = busy ? 'Loading…' : label; button.classList.toggle('opacity-60', busy); button.classList.toggle('cursor-not-allowed', busy); }
async function load() {
  setStatus('Loading UMAP and cluster data…');
  try {
    const response = await fetch('/api/umap'); if (!response.ok) throw new Error(`Data request failed (${response.status})`); umapData = (await response.json()).cells; if (!umapData.length) throw new Error('The dataset returned no cells.');
  } catch (error) { $('plot').innerHTML = '<div class="flex h-full items-center justify-center p-6 text-center text-red-300">The dataset could not be loaded.</div>'; setStatus(`${error.message} Check that the app is running and the H5AD file is available.`, 'error'); return; }
  const clusters = [...new Set(umapData.map(d => d.cluster))].sort((a,b) => +a - +b);
  $('cluster').innerHTML = clusters.map(c => `<option>${c}</option>`).join('');
  try { const geneResponse = await fetch('/api/genes'); if (!geneResponse.ok) throw new Error(`Gene list request failed (${geneResponse.status}).`); const geneList = (await geneResponse.json()).genes; $('geneSelect').innerHTML = geneList.map(g => `<option value="${g}">${g}</option>`).join(''); $('geneSelect').value = 'LST1'; $('geneSelect').addEventListener('change', () => { $('gene').value = $('geneSelect').value; plotGene(); }); } catch (error) { $('geneSelect').innerHTML = '<option>Gene list unavailable</option>'; setStatus(error.message, 'error'); }
  $('colorBy').addEventListener('change', () => { draw(); });
  $('geneBtn').addEventListener('click', plotGene);
  $('gene').addEventListener('keydown', event => { if (event.key === 'Enter') plotGene(); });
  $('cluster').addEventListener('change', loadMarkers);
  document.querySelectorAll('.cluster-quick').forEach(button => button.addEventListener('click', () => { $('cluster').value = button.dataset.cluster; drawCluster(button.dataset.cluster); loadMarkers(); }));
  draw(); await loadOverview(); await loadMarkers(); await plotGene(); setStatus('Ready. Hover over cells or choose another view.', 'success');
}
function colorLabel(mode) { return mode === 'cluster' ? 'Leiden cluster' : mode === 'n_genes' ? 'Number of genes detected per cell' : 'Percentage of mitochondrial counts'; }
function setActiveView(label) { $('activeView').textContent = `Active coloring: ${label}`; }
function setGeneView(gene) { $('colorBy').value = 'cluster'; setActiveView(`${gene} expression (log-normalized)`); }
function drawCluster(cluster) { $('colorBy').value = 'cluster'; const clusters = [...new Set(umapData.map(d => d.cluster))].sort((a,b)=>+a-+b); const traces = clusters.map((c,i) => { const z=umapData.filter(d=>d.cluster===c); const selected = c === cluster; return {x:z.map(d=>d.x),y:z.map(d=>d.y),mode:'markers',type:'scattergl',name:`Cluster ${c}`,text:z.map(d=>`${d.cell_id}<br>Cluster: ${c}<br>Number of genes: ${d.n_genes}<br>Percentage of mitochondria: ${d.pct_mito.toFixed(2)}%`),hoverinfo:'text',marker:{color:palette[i%palette.length],size:selected?9:5,opacity:selected?1:.18,line:{color:selected?'#ffffff':'#0f172a',width:selected?1.5:.2}}}; }); Plotly.newPlot('plot',traces,layout(`UMAP — Cluster ${cluster} highlighted`),{responsive:true,displaylogo:false}); setActiveView(`Leiden cluster — Cluster ${cluster} highlighted`); }
function draw() {
  const mode = $('colorBy').value;
  setActiveView(colorLabel(mode));
  if (mode === 'cluster') {
    const traces = [...new Set(umapData.map(d => d.cluster))].sort((a,b)=>+a-+b).map((c,i) => { const z=umapData.filter(d=>d.cluster===c); return {x:z.map(d=>d.x),y:z.map(d=>d.y),mode:'markers',type:'scattergl',name:`Cluster ${c}`,text:z.map(d=>`${d.cell_id}<br>Number of genes: ${d.n_genes}<br>Percentage of mitochondria: ${d.pct_mito.toFixed(2)}%`),hoverinfo:'text',marker:{color:palette[i%palette.length],size:6,opacity:.8}}; }); Plotly.newPlot('plot',traces,layout('UMAP — Leiden clusters'),{responsive:true,displaylogo:false});
  } else { const vals=umapData.map(d=>d[mode]); Plotly.newPlot('plot',[{x:umapData.map(d=>d.x),y:umapData.map(d=>d.y),mode:'markers',type:'scattergl',text:umapData.map(d=>`${d.cell_id}<br>${mode === 'n_genes' ? 'Number of genes' : 'Percentage of mitochondria'}: ${mode === 'n_genes' ? d.n_genes : d.pct_mito.toFixed(2) + '%'}`),hoverinfo:'text',marker:{color:vals,colorscale:'Cividis',size:6,line:{color:'#0f172a',width:.2},colorbar:{title:mode === 'n_genes' ? 'Number of genes' : 'Percentage of mitochondria',titlefont:{color:'#f8fafc'},tickfont:{color:'#cbd5e1'}}}}],layout(mode === 'n_genes' ? 'UMAP — Number of genes<br>detected per cell' : 'UMAP — Percentage of<br>mitochondria'),{responsive:true,displaylogo:false}); }
}
function layout(title) { return {title:{text:title,font:{color:'#f8fafc',size:16}},paper_bgcolor:'#0f172a',plot_bgcolor:'#0f172a',font:{color:'#cbd5e1'},margin:{l:58,r:28,t:58,b:52},xaxis:{title:'UMAP 1 (arbitrary units)',gridcolor:'#334155',zerolinecolor:'#475569'},yaxis:{title:'UMAP 2 (arbitrary units)',gridcolor:'#334155',zerolinecolor:'#475569'}}; }
async function plotGene() { const gene=($('gene').value.trim() || $('geneSelect').value || '').toUpperCase(); if(!gene){setStatus('Type a gene symbol before selecting Show gene.', 'error'); $('gene').focus(); return false;} const button=$('geneBtn'); setBusy(button, true, 'Show gene'); setStatus(`Loading ${gene} expression…`); try { const r=await fetch(`/api/genes/${encodeURIComponent(gene)}`); if(r.status===404) throw new Error(`Gene not found: ${gene} is not in this dataset. Try FCER1G, LST1, or CD3D.`); if(!r.ok) throw new Error(`Expression request failed (${r.status}).`); const payload=await r.json(); if(!payload.values?.length) throw new Error(`No expression values were returned for ${gene}.`); const byId=new Map(payload.values.map(d=>[d.cell_id,d.expression])); Plotly.newPlot('plot',[{x:umapData.map(d=>d.x),y:umapData.map(d=>d.y),mode:'markers',type:'scattergl',name:`${gene} expression (log-normalized)`,text:umapData.map(d=>`${d.cell_id}<br>${gene} (log-normalized): ${byId.get(d.cell_id).toFixed(3)}`),hoverinfo:'text',marker:{color:umapData.map(d=>byId.get(d.cell_id)),colorscale:'Cividis',size:6,line:{color:'#0f172a',width:.2},colorbar:{title:`${gene} (log-normalized)`,titlefont:{color:'#f8fafc'},tickfont:{color:'#cbd5e1'}}}}],layout(`UMAP — ${gene}<br>expression (log-normalized)`),{responsive:true,displaylogo:false}); setGeneView(gene); setStatus(`${gene} loaded. Values are log-normalized expression from adata.X.`, 'success'); return true; } catch(error) { setStatus(error.message, 'error'); return false; } finally { setBusy(button, false, 'Show gene'); } }
async function loadOverview() { try { const r=await fetch('/api/clusters/overview'); if(!r.ok) throw new Error(`Cluster overview request failed (${r.status}).`); const d=await r.json(); $('overview').innerHTML=d.clusters.map(item=>`<tr class="border-t border-slate-800"><td class="px-4 py-2 font-medium">${item.cluster}</td><td class="px-4 py-2">${item.n_cells}</td><td class="px-4 py-2">${item.median_detected_genes.toFixed(0)}</td><td class="px-4 py-2">${item.median_mitochondrial_percentage.toFixed(2)}%</td><td class="px-4 py-2">${item.top_markers.join(', ')}</td></tr>`).join(''); } catch(error) { $('overview').innerHTML=`<tr><td colspan="5" class="px-4 py-3 text-red-300">${error.message}</td></tr>`; setStatus(error.message, 'error'); } }
async function loadMarkers() { const c=$('cluster').value; if(c===undefined)return; $('quality').innerHTML='Loading cluster quality and markers…'; try { const r=await fetch(`/api/clusters/${c}/markers?n_genes=15`); if(!r.ok) throw new Error(`Marker request failed (${r.status}).`); const d=await r.json(); $('quality').innerHTML=`<b>Cluster ${c}</b><br>${d.n_cells} cells<br>Number of genes median: ${d.quality.n_genes_median.toFixed(0)} [${d.quality.n_genes_range.join('–')}]<br>Percentage of mitochondria median: ${d.quality.pct_mito_median.toFixed(2)}% [${d.quality.pct_mito_range.map(x=>x.toFixed(2)).join('–')}%]`; $('markers').innerHTML=d.markers.map(m=>`<tr class="border-t border-slate-800"><td class="px-4 py-2 font-medium">${m.gene}</td><td class="px-4 py-2">${m.score.toFixed(2)}</td><td class="px-4 py-2">${m.logfoldchange.toFixed(2)}</td><td class="px-4 py-2">${m.pval_adj.toExponential(2)}</td></tr>`).join(''); } catch(error) { $('quality').textContent=error.message; $('markers').innerHTML=''; setStatus(error.message, 'error'); } }
load();
</script>
</body></html>'''
