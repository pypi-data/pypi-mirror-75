# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:27 2020

@author: Gideon Pomeranz

Run preprocessing for data from the align command

Arguments:
    -o (organism name)
    -f file that holds info on the samples
    --min_cells (no. of threads for kb count, default = 2)
    --min_genes (amount of memory, default = 8)
    --mito_criteria
    --max_genes
    --n_top_genes
"""

### Packages ###
import os  # run system function
import anndata
import scanpy as sc
from .utils import create_batch_adata,populate,t2g, run_qc, filtering
from harmony import harmonize

#----------------------------------------------------------------------------#
def preprocess(file,organism, min_cells,min_genes,mito_criteria,max_genes,n_top_genes):
    ## Sample information ##
    # read in the batch.txt file that holds sample names and ftp connections
    batch_file = open(file,"r")
    
    samples = []
    index = 0
    # loop through each line to get each sample information
    print("File contents:")
    for line in batch_file:
        current_line = line.strip()  # this removes any whitespace characters
        current_line = current_line.split(" ")
        print(current_line)
        samples.append(current_line)
        index += 1
    
    # close file connection
    batch_file.close()
    
    # remove the first line which is just the column information
    samples.pop(0)
    
    #------------------------------------------------------------------------#
    
    ### Anndata ###
    print("Creating Anndata object")
    
    # this directory is going to hold the final anndata objects to be concatanated
    my_data = {}
    # this directory is going to hold all raw data before writing it to disk
    raw_data ={}
    # get unique entries for names from samples[0]
    sample_names =[]
    for sample in samples:
        sample_names.append(sample[0])
    
    unique_samples = list(set(sample_names))
    
    # testing 
    # unique = "DN3"
    
    for unique in unique_samples:
        # this function concatanetes multiple batches of the same sample into
        # one anndata object
        temp_data = create_batch_adata(unique,sample_names)
        
        ## Transcripts to Genes ##
        organism = "human"
        # this functions adds the gene names to temp_data
        # it adds to entries to adata.var: gene_id (which are the ensembl ids) 
        # and gene_name (which are the common gene names)
        temp_data = t2g(temp_data)
        
        print("Prefiltered adata:", temp_data)
        
        # Populate adata with information
        temp_data = populate(temp_data,organism)
        
        # make variable names unique
        temp_data.var_names_make_unique()
        temp_data.obs_names_make_unique()
        #--------------------------------------------------------------------#
        # Filter adata based on following criteria
        min_cells = min_cells
        min_genes = min_genes
        max_genes = max_genes
        mito_criteria = mito_criteria
        
        filtering(temp_data, min_cells, min_genes, mito_criteria,organism, \
                  max_genes)
        #--------------------------------------------------------------------#
        # add to raw_data for later saving of concatanated raw files
        raw_data[unique] = temp_data
        #--------------------------------------------------------------------#
        ### Normalisation and Log transform ###
        temp_data.raw = temp_data
        # Normalise
        sc.pp.normalize_total(temp_data, target_sum=1e6)
        #Log transform
        sc.pp.log1p(temp_data)
        #---------------------------------------------------------------------#
        ### Highly variable genes ###
        sc.pp.highly_variable_genes(temp_data,n_top_genes=n_top_genes,batch_key="Batches")
        
        # filter data to highly variabel genes only
        highly_variable_genes=temp_data.var["highly_variable"]
        temp_data = temp_data[:,highly_variable_genes]
        
        # remove noise from number of counts and mitochondrial content
        sc.pp.regress_out(temp_data, ["cell_counts","percent_mito"])
        # scale data to unit variance and zero mean
        sc.pp.scale(temp_data)
        #--------------------------------------------------------------------#
        ### Harmony batch correction ###
        ## Preprocess PCA ##
        sc.pp.pca(temp_data,svd_solver="arpack")
        Z = harmonize(temp_data.obsm["X_pca"], temp_data.obs, batch_key = "Batches")
        temp_data.obsm['X_harmony'] = Z
        
        #--------------------------------------------------------------------#
        print("Filtered/Corrected adata:", temp_data)
        # add to my_data
        my_data[unique] = temp_data
    #------------------------------------------------------------------------#
        
    # Concatanate all the samples together
    adata_raw = anndata.concat(raw_data, label="Samples", join="inner")
    adata_raw.obs_names_make_unique()
    adata = anndata.concat(my_data, label="Samples", join="inner")
    adata.obs_names_make_unique()
    #------------------------------------------------------------------------#
    ## Run QC Plots for raw and corrected##
    print("Running QC plots")
    # make new qc plot statements where we temporarily assign values to anndata
    run_qc(adata_raw,directory_name="qc_plots", sample="complete")
    
    # Rerun PCA for complete set
    sc.pp.pca(adata,svd_solver="arpack")
    run_qc(adata,directory_name="filtered_qc_plots", sample="complete", \
           mito_criteria = mito_criteria,filtered=True)
    #------------------------------------------------------------------------#
    ### Save datasets ###
    os.makedirs("write",exist_ok=True)
    raw_file = './write/raw.h5ad'
    processed_file = './write/processed.h5ad'
    
    adata.write_h5ad(raw_file)
    adata_raw.write_h5ad(processed_file)
