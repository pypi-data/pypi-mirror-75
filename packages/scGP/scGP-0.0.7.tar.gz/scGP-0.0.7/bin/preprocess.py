# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 20:28:27 2020

@author: Gideon Pomeranz

Run Pseudoalignment on scRNA-seq Data using Kallisto Bustools and Scanpy

Arguments:
    -o (organism name)
    -f file that holds info on the samples
    -x (technology)
    --threads (no. of threads for kb count, default = 2)
    --memory (amount of memory, default = 8)
"""

### Packages ###
import os  # run system function
import anndata
import pandas as pd
import scanpy as sc
from utils import (create_batch_adata,populate,t2g, run_qc, filtering)
import qc_plot_functions

#----------------------------------------------------------------------------#
### Argparser ###
import argparse



#----------------------------------------------------------------------------#
### Kallisto-Bustools ###
print("Running Kallisto-Bustools")

## KB ref ##
print(["Downloading Kallisto index for", args.o])
if (os.path.isfile("index.idx") + os.path.isfile("t2g.txt")) != int(2):
    # this downloads a kallisto index
    os.system(" ".join(["kb ref -d", args.o, "-i index.idx -g t2g.txt -f1 transcriptome.fasta"]))

## KB count ##
# read in the batch.txt file that holds sample names and ftp connections
batch_file = open(args.f,"r")

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


# run the loop that will run kb count on each sample
print("Running Kb count")
directories = []
for sample in samples:
    sample_folder_name = sample[0]  # This is the sample name i.e DN2
    batch_folder_name = sample[1]  # This is the batch number i.e. 0
    kb_count_directory = "/".join([sample_folder_name,"_".join(["batch", batch_folder_name])])
    directories.append(kb_count_directory)
    fasta_files = " ".join(sample[2:])  # These are the fasta files
    os.system(" ".join( \
        ["kb count --verbose --h5ad -i index.idx -g t2g.txt -x", args.x, "-o", \
         kb_count_directory , "--filter bustools -t", args.t, "-m",args.mem, fasta_files]))

#----------------------------------------------------------------------------#

### Anndata ###
print("Creating Anndata object")

# this directory is going to hold the final anndata objects to be concatanated
my_data = {}
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
    temp_data = populate(temp_data,organism=organism)
    
    print("Current adata:", temp_data)
    
    # add to my_data
    my_data[unique] = temp_data
    
#----------------------------------------------------------------------------#
## Run QC Plots ##
print("Running QC plots")
# make new qc plot statements where we temporarily assign values to anndata
run_qc(temp_data,directory_name="qc_plots", unique=unique)
#----------------------------------------------------------------------------#
### Save raw data






### Filtering ###
# continue filtering with default values
min_genes = 500
max_genes = 2500
min_cells = 3
mito_criteria = 20

filtering(temp_data, min_genes, max_genes, min_cells, mito_criteria, organism)
#----------------------------------------------------------------------------#
### Normalisation and Log transform ###
temp_data.raw = temp_data
# Normalise
sc.pp.normalize_total(temp_data, target_sum=1e6)
#Log transform
sc.pp.log1p(temp_data)
    