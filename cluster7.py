import scanpy as sc,numpy as np
x=sc.read_h5ad('ddls_tmp/data/pbmc3k.h5ad'); X=x.X.toarray() if hasattr(x.X,'toarray') else np.asarray(x.X)
sc.tl.rank_genes_groups(x,'leiden',groups=['7'],reference='rest',method='wilcoxon',n_genes=20,use_raw=False)
d=x.uns['rank_genes_groups']; genes=list(d['names']['7'])
print('| Rank | Gene | C0 | C1 | C2 | C3 | C4 | C5 | C6 | C7 |')
print('|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for k,g in enumerate(genes):
 j=x.var_names.get_loc(g); vals=[]
 for c in map(str,range(8)):
  z=X[x.obs.leiden==c,j]; vals.append(z.mean())
 print(f"| {k+1} | **{g}** | " + ' | '.join(f'{v:.2f}' for v in vals) + ' |')
print('\nmarkers')
for k,g in enumerate(genes): print(k+1,g,float(d['scores']['7'][k]),float(d['logfoldchanges']['7'][k]),float(d['pvals_adj']['7'][k]))
