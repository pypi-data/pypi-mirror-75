#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################
"""
Shared functions used along ``BacterialTyper`` & ``XICRA`` pipeline.
With different purposes:
    - Print time stamps
  
    - Create system calls

    - Manage/list/arrange files/folders

    - Aesthetics

    - Manage fasta files

    - Other miscellaneous functions
"""
## useful imports
from termcolor import colored
import os

from HCGB.functions import system_call_functions

##########################
###        BLAST       ###
##########################

###############
def makeblastdb(DBname, fasta, makeblastDBexe):
    ## generate blastdb for genome
    if (os.path.isfile(DBname + '.nhr')):
        print ("+ BLAST database is already generated...")
    else:
        cmd_makeblast = "%s -in %s -input_type fasta -dbtype %s -out %s" %(makeblastDBexe, fasta, 'nucl', DBname)
        code = system_call_functions.system_call(cmd_makeblast)

        if (code == 'FAIL'):
            print (colored('****ERROR: Some error happened during the makeblastDB command', 'red'))
            print (cmd_makeblast)
            exit()
    

###############    
def blastn(blastnexe, outFile, DBname, fasta, threads):
    # blastn plasmids vs contigs
    cmd_blastn = "%s -db %s -query %s -out %s -evalue 1e-20 -outfmt \'6 std qlen slen\' -num_threads %s" %(blastnexe, DBname, fasta, outFile, threads )
    codeBlastn = system_call_functions.system_call(cmd_blastn)
    
    if (codeBlastn == 'FAIL'):
        print (colored('****ERROR: Some error happened during the blastn command', 'red'))
        print (cmd_blastn)
        exit()