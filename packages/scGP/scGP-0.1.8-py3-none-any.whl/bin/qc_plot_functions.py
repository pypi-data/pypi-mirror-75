# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:29:34 2020

@author: Gideon Pomeranz

Title: qc_plots

Description: This script holds the functions for 4 qc plots

"""
# Packages
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scanpy as sc
#----------------------------------------------------------------------------#
def nd(arr):
    return np.asarray(arr).reshape(-1)
#----------------------------------------------------------------------------#
# Knee plot
def knee_plot(adata, directory):
    expected_num_cells = 3000
    knee = np.sort(nd(adata.X.sum(axis=1)))[::-1]
    
    fig, ax = plt.subplots(figsize=(5, 5))
    
    x = knee
    y = range(len(knee))
    
    ax.loglog(x, y, linewidth=5, color="g")
    
    ax.axvline(x=knee[expected_num_cells], linewidth=3, color="k")
    ax.axhline(y=expected_num_cells, linewidth=3, color="k")
    
    ax.set_xlabel("UMI Counts")
    ax.set_ylabel("Set of Barcodes")
    
    plt.savefig("".join([directory, "/knee_plot.png"]))
    plt.clf()
#----------------------------------------------------------------------------#
# Mitochondrial content
def mito_content(adata,mito_criteria,directory):
    fig, ax = plt.subplots(figsize=(5,5))

    x = nd(adata.obs["cell_counts"])
    y = nd(adata.obs["percent_mito"])
    
    ax.scatter(x, y, color="green", alpha=0.25)
    
    if mito_criteria != None:
        ax.axhline(y=mito_criteria, linestyle="--", color="k")
    
    ax.set_xlabel("UMI Counts")
    ax.set_ylabel("Percent mito")
    
    plt.savefig("".join([directory, "/Mito_content.png"]))
    plt.clf()
#----------------------------------------------------------------------------#
# Library saturation 1
def library_saturation_1(data, directory):
    fig, ax = plt.subplots(figsize=(5, 5))

    x = nd(data.X.sum(axis=1))
    y = nd(np.sum(data.X>0, axis=1))
    
    ax.scatter(x, y, color="green", alpha=0.25)
    
    ax.set_xlabel("UMI Counts")
    ax.set_ylabel("Genes Detected")
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    ax.set_xlim(1)
    ax.set_ylim(1)
    
    plt.savefig("".join([directory, "/libary_saturation_1.png"]))
    plt.clf()
#----------------------------------------------------------------------------#    
def library_saturation_2(data, directory):
    fig, ax = plt.subplots(figsize=(5,5))
    
    x = nd(data.X.sum(axis=1))
    y = nd(np.sum(data.X>0, axis=1))

    #histogram definition
    bins = [1500, 1500] # number of bins
    
    # histogram the data
    hh, locx, locy = np.histogram2d(x, y, bins=bins)
    
    # Sort the points by density, so that the densest points are plotted last
    z = np.array([hh[np.argmax(a<=locx[1:]),np.argmax(b<=locy[1:])] for a,b in zip(x,y)])
    idx = z.argsort()
    x2, y2, z2 = x[idx], y[idx], z[idx]
    
    s = ax.scatter(x2, y2, c=z2, cmap='Greens')  
    fig.colorbar(s, ax=ax)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("UMI Counts")
    ax.set_ylabel("Genes Detected")
    
    ax.set_xlim(1, 10**5)
    ax.set_ylim(1, 10**4)
    
    plt.savefig("".join([directory, "/library_saturation_2.png"]))
    plt.clf()
#----------------------------------------------------------------------------#
# This plot is for after putting in parameters it shows the highest expressed genes
def highest_expr_genes(data,directory):
    fig, ax = plt.subplots(figsize=(5, 10))
    sc.pl.highest_expr_genes(data, n_top=20, ax = ax)
    
    plt.savefig("".join([directory,"/highest_expr_genes.png"]))
    plt.clf()
#----------------------------------------------------------------------------# 
def pca_var_expl_ratio(data,directory):
    fig, ax = plt.subplots(figsize=(5, 5))
    sc.pl.pca_variance_ratio(data,n_pcs=50)
    
    plt.savefig("".join([directory,"/pca_variance_explained.png"]))
    plt.clf()
#----------------------------------------------------------------------------#
# taken from https://stats.stackexchange.com/questions/12819/how-to-draw-a-scree-plot-in-python
def scree_plot(num_PCA,eigvals,directory):
    fig = plt.figure(figsize=(8,6))
    sing_vals = np.arange(num_PCA) + 1
    plt.plot(sing_vals, eigvals, 'ro-', linewidth=2)
    plt.title('Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Eigenvalue')
    #I don't like the default legend so I typically make mine like below, e.g.
    #with smaller fonts and a bit transparent so I do not cover up data, and make
    #it moveable by the viewer in case upper-right is a bad place for it 
    leg = plt.legend(['Eigenvalues from SVD'], loc='best', borderpad=0.3, 
                     shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
                     markerscale=0.4)
    leg.get_frame().set_alpha(0.4)
    
    plt.savefig("".join([directory,"/scree_plot.png"]))
    plt.clf()