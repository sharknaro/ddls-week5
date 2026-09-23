import scanpy as sc,numpy as np,pandas as pd
x=sc.read_h5ad('ddls_tmp/data/pbmc3k.h5ad'); X=x.X.toarray() if hasattr(x.X,'toarray') else np.asarray(x.X); C=x.layers['counts']; C=C.toarray() if hasattr(C,'toarray') else np.asarray(C)
print('X range',X.min(),X.max(),'counts range',C.min(),C.max(),'finite',np.isfinite(X).all(),np.isfinite(C).all())
print('obs summary',x.obs.describe(include='all').to_string())
print('var metadata',x.var[['mt','n_cells_by_counts','mean_counts','pct_dropout_by_counts','total_counts','highly_variable']].describe(include='all').to_string())
print('X nonzero per cell summary', (X>0).sum(1).min(),np.median((X>0).sum(1)),(X>0).max())
print('counts nonzero per cell summary', (C>0).sum(1).min(),np.median((C>0).sum(1)),(C>0).max())
print('doublet cols',[c for c in x.obs if 'double' in c.lower() or 'scrub' in c.lower()])
# recommended flags, explicit not original
obs=x.obs.copy();
for col in ['n_genes','total_counts','pct_mito']:
 print(col,'q01 q05 q25 q50 q75 q95 q99',obs[col].quantile([.01,.05,.25,.5,.75,.95,.99]).round(3).to_dict())
# conventional pbmc tutorial thresholds n_genes<200, pct mito>5
flags=pd.DataFrame(index=x.obs_names);flags['low_genes_lt200']=obs.n_genes<200;flags['high_mito_gt5']=obs.pct_mito>5;flags['low_counts_lt500']=obs.total_counts<500;flags['high_genes_gt2500']=obs.n_genes>2500
print('flags',flags.sum().to_dict())
print('flag overlap',pd.crosstab(flags.low_genes_lt200,flags.high_mito_gt5))
print('flag by cluster',pd.concat([obs.leiden,flags],axis=1).groupby('leiden',observed=True).sum().to_string())
# top prevalence genes
prev=(X>0).mean(0); print('top prevalence',sorted(zip(x.var_names,prev),key=lambda z:-z[1])[:20])
