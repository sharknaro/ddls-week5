import scanpy as sc,pandas as pd,numpy as np
x=sc.read_h5ad('ddls_tmp/data/pbmc3k.h5ad'); X=x.X.toarray() if hasattr(x.X,'toarray') else np.asarray(x.X)
sc.tl.rank_genes_groups(x,'leiden',groups=['4'],reference='rest',method='wilcoxon',n_genes=20,use_raw=False)
d=x.uns['rank_genes_groups']; genes=list(d['names']['4'])
print('gene,score,lfc,padj,'+','.join('mean_'+str(i) for i in range(8))+','+','.join('pct_'+str(i) for i in range(8)))
for k,g in enumerate(genes):
 j=x.var_names.get_loc(g); means=[]; pcts=[]
 for c in map(str,range(8)):
  z=X[x.obs.leiden==c,j]; means.append(z.mean()); pcts.append((z>0).mean())
 print(g, d['scores']['4'][k], d['logfoldchanges']['4'][k],d['pvals_adj']['4'][k],*means,*pcts,sep=',')
print('\nQC cluster')
print(x.obs.groupby('leiden',observed=True)[['n_genes','total_counts','pct_mito']].agg(['mean','median','min','max']).to_string())
