# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 21:23:32 2020

@author: Gideon Pomeranz

scGP align 



"""
### Packages ###
import os

#----------------------------------------------------------------------------#
def align(file,organism,technology,threads,memory):
    ### Kallisto-Bustools ###
    print("Running Kallisto-Bustools")
    
    ## KB ref ##
    print(["Downloading Kallisto index for", organism])
    if (os.path.isfile("index.idx") + os.path.isfile("t2g.txt")) != int(2):
        # this downloads a kallisto index
        os.system(" ".join(["kb ref -d", organism, \
                            "-i index.idx -g t2g.txt -f1 transcriptome.fasta"]))
    
    ## KB count ##
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
    
    
    # run the loop that will run kb count on each sample
    print("Running Kb count")
    directories = []
    for sample in samples:
        #sample_folder_name = sample[0]  # This is the sample name i.e DN2
        #batch_folder_name = sample[1]  # This is the batch number i.e. 0
        #kb_count_directory = "/".join([sample_folder_name,"_".join(["batch", batch_folder_name])])
        #directories.append(kb_count_directory)
        kb_count_directory = "_".join([sample[0],sample[1]])
        fasta_files = " ".join(sample[2:])  # These are the fasta files
        os.system(" ".join(
            ["kb count --verbose --h5ad -i index.idx -g t2g.txt -x", technology, "-o", \
             kb_count_directory , "--filter bustools -t", threads, "-m", memory, fasta_files]))
    
    print("Completed Pseudoalignment using KB")

#----------------------------------------------------------------------------#