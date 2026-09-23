import scanpy as sc,pandas as pd,numpy as np
x=sc.read_h5ad('ddls_tmp/data/pbmc3k.h5ad')
genes=['LST1','FCER1G','FCGR3A','COTL1','AIF1','IFITM2','IFITM3','FTH1','SAT1','SERPINA1','FTL','PSAP','CTSS','S100A11','OAZ1','RP11-290F20.3','CD68','S100A4','TIMP1','CST3']
missing=[g for g in genes if g not in x.var_names]; print('missing',missing)
X=x.X.toarray() if hasattr(x.X,'toarray') else np.asarray(x.X)
C=x.layers['counts']; C=C.toarray() if hasattr(C,'toarray') else np.asarray(C)
base=pd.DataFrame({'cell_id':x.obs_names.astype(str),'cluster':x.obs['leiden'].astype(str).values,'n_genes':x.obs['n_genes'].values,'pct_mito':x.obs['pct_mito'].values})
for g in genes:
 j=x.var_names.get_loc(g); base[g+'_expr']=X[:,j]; base[g+'_detected']=(C[:,j]>0).astype(int)
base.to_csv('cluster4_per_cell_compact.csv',index=False)
# print sample
print(base.head().to_string(index=False))
print('shape',base.shape)
print('file bytes',__import__('os').path.getsize('cluster4_per_cell_compact.csv'))
