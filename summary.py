import scanpy as sc,numpy as np,pandas as pd
x=sc.read_h5ad('ddls_tmp/data/pbmc3k.h5ad'); C=x.layers['counts']; C=C.toarray() if hasattr(C,'toarray') else np.asarray(C)
obs=x.obs
for cl,genes in [('4',['LST1','FCER1G','FCGR3A','AIF1','CTSS','CD68','CST3']),('7',['STMN1','PCNA','TYMS','KIAA0101'])]:
 ix=np.array(obs.leiden==cl); sub=obs.iloc[ix]; ids=[x.var_names.get_loc(g) for g in genes]; d=C[ix][:,ids]>0
 print('\nCL',cl,'n',ix.sum())
 for col in ['n_genes','pct_mito']:
  print(col,'median',np.median(sub[col]),'range',sub[col].min(),sub[col].max())
 print('any',d.any(1).sum(),'atleast3',(d.sum(1)>=3).sum(),'counts',d.sum(1).tolist())
 # strong nonmyeloid markers cluster4: B/T/NK/platelet marker at >=1 among selected
 nm=['CD3D','CD3E','MS4A1','CD79A','NKG7','GNLY','CCL5','GZMB','PPBP','PF4','MKI67']
 nm=[g for g in nm if g in x.var_names]; j=[x.var_names.get_loc(g) for g in nm]; z=C[ix][:,j]>0
 print('nonmyeloid any',z.any(1).sum(),'genes',[(g,int(z[:,k].sum())) for k,g in enumerate(nm)])
 # doublet heuristic high genes >2500 or high total >? report no official
 print('highgenes',int((sub.n_genes>2500).sum()),'max',sub.n_genes.max())
 print('rows',list(zip(sub.index,d.sum(1))))
