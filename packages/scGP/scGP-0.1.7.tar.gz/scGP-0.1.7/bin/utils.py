# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:57:57 2020

@author: Gideon Pomeranz

Utility functions for main

"""
### Packages ###
import os
import scanpy as sc
import pandas as pd
import numpy as np
import anndata
from .qc_plot_functions import knee_plot,mito_content,library_saturation_1,library_saturation_2,highest_expr_genes,pca_var_expl_ratio

# Helper function
def nd(arr):
    return np.asarray(arr).reshape(-1)



#----------------------------------------------------------------------------#
def create_batch_adata(unique,sample_names):
    unique = str(unique)
    print("Sample name:", unique)
    pre_indeces = [i for i, e in enumerate(sample_names) if e == unique]
    
    indeces = list(range(0,len(pre_indeces)))
    
    print("Batches:", indeces)
    
    # setup reading in of the pseudoaligned files
    count = 0
    temp_dir = {}
    for index in indeces:
        variable_name = "_".join([unique,str(count)])
        directory_name = "/".join([unique,str(count)])
        print("Reading in counts for:", unique, ",Batch number", str(count))
        temp_dir[variable_name] = anndata.read_h5ad( \
            "".join([variable_name,"/counts_unfiltered/adata.h5ad"]))  # change to directory_name
        
        count += 1
        
        
    # make into one anndata object with the temp_dir index being the batch index
    b_categories=list(temp_dir.keys())
    if len(b_categories) == 1:
        temp_data = temp_dir[b_categories[0]]
    else:
        temp_data = anndata.concat(temp_dir, label="Batches", join="inner")
        
    
    return(temp_data)

#----------------------------------------------------------------------------#
def populate(adata,organism):

    # populate anndata object with information
    adata.obs["cell_counts"] = adata.X.sum(axis=1)
    adata.var["gene_counts"] = nd(adata.X.sum(axis=0))
    
    adata.obs["n_genes"] = nd((adata.X>0).sum(axis=1))
    adata.var["n_cells"] = nd((adata.X>0).sum(axis=0))
    
    # quick conditional to differentiate between human and mouse (fish?)
    if organism == "human":
        organism_specific_mito_name = "MT-"
    else:
        organism_specific_mito_name = "mt-"
    mito_genes = adata.var_names.str.startswith(organism_specific_mito_name)
    adata.obs["percent_mito"] = adata[:,mito_genes].X.sum(axis=1)/adata.X.sum(axis=1)*100
    return(adata)
#----------------------------------------------------------------------------#
def t2g(adata):
    adata.var["gene_id"] = adata.var.index.values

    t2g = pd.read_csv("t2g.txt", header=None, names=["tid", "gene_id", "gene_name"], sep="\t")
    t2g.index = t2g.gene_id
    t2g = t2g.loc[~t2g.index.duplicated(keep='first')]
    
    adata.var["gene_name"] = adata.var.gene_id.map(t2g["gene_name"])
    adata.var.index = adata.var["gene_name"]
    
    return(adata)

#----------------------------------------------------------------------------#
def run_qc(adata,directory_name,sample,mito_criteria=None, filtered=False):
    
    plot_directory = directory_name
    os.makedirs(plot_directory, exist_ok=True)
    os.makedirs("/".join([plot_directory, sample]), exist_ok=True)
    plot_directory = "/".join([plot_directory, sample])
    # because this is before filtering
    mito_criteria=mito_criteria
    
    knee_plot(adata,plot_directory)
    mito_content(adata,mito_criteria,plot_directory)
    library_saturation_1(adata,plot_directory)
    library_saturation_2(adata,plot_directory)
    
    if filtered == True:
        #sc._settings.ScanpyConfig.figdir = plot_directory
        sc.pl.highest_expr_genes(adata, n_top=20, save=True)
        sc.pl.pca_var_expl_ratio(adata, n_pcs=50, save=True)
#----------------------------------------------------------------------------#
def filtering(adata,min_cells, min_genes, mito_criteria, organism, max_genes):
    
    sc.pp.filter_cells(adata,min_genes=min_genes)
    sc.pp.filter_genes(adata,min_cells=min_cells)
    sc.pp.filter_cells(adata, min_genes=1)
    
    if organism == "human":
        organism_specific_mito_name = "MT-"
    else:
        organism_specific_mito_name = "mt-"
    
    mito_genes = adata.var_names.str.startswith(organism_specific_mito_name)
    adata.obs["percent_mito"] = ( \
        np.sum(adata[:, mito_genes].X, axis=1).A1 / np.sum(adata.X, axis=1).A1)
        
    adata.obs["n_counts"] = adata.X.sum(axis=1).A1
    
    # Filter by too many expressed genes, in this case 2500
    adata = adata[adata.obs["n_genes"] < int(max_genes), :]
    adata = adata[adata.obs["percent_mito"] < mito_criteria, :]