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
import os
import pandas as pd

###################################
##     General main functions    ##
###################################

#################
def print_all_pandaDF(pd_df):
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)
    print (pd_df)

#################
def printList2file(fileGiven, listGiven):
    """Prints list given in the output file provided. One item per row."""
    file_hd = open(fileGiven, 'w')
    file_hd.write("\n".join(listGiven))
    file_hd.close()  

#################
def readList_fromFile(fileGiven):
    """Reads list from the input file provided. One item per row."""
    # open file and read content into list
    lineList = [line.rstrip('\n') for line in open(fileGiven)]
    return (lineList)

###########
def retrieve_matching_files(folder, string):
    """Lists folder path provided and given a string to search, returns all files ending with the given string"""
    my_all_list = get_fullpath_list(folder)
    matching = [s for s in my_all_list if s.endswith(string)]
    return (matching)

##########
def file2dictionary(file2read, split_char):
    """Read file and generate a dictionary"""
    d = {}
    with open(file2read) as f:
        for line in f:
            line = line.rstrip('\n')
            (key, val) = line.split(split_char)
            d[key] = val

    return(d)

###############
def file2dataframe(file2read, names):
    ## TODO: check if duplicated with get_data function
    """Read csv file into pandas dataframe"""
    d = pd.read_csv(file2read, comment="#", names=names)
    return(d)

#################
def get_fullpath_list(dir_given, Debug):
    """Retrieve full absolute path for the files within a directory specified.

    :param dir_given: Directory to retrieve files
    :type dir_given: string

    :returns: List of absolute path files.
    """
    return_path = []
    for root, dirs, files in os.walk(dir_given):
        for f in files:
            return_path.append(os.path.join(root,f))

    if Debug:
        print ("** DEBUG:\nroot: ", root)
        print ("Dirs: ")
        print (dirs)
        print ("Files: ")
        print (files)
    
    ## returns list of files
    return return_path

###############
def get_data(ID_file, SEP, options):    
    if options == 'index_col=0':
        data = pd.read_csv(ID_file, sep=SEP, index_col=0)
        return(data)
    else:
        data = pd.read_csv(ID_file, sep=SEP)
        return(data)
    ## fix for another example if any
    
###############
def get_number_lines(input_file):    
    with open(input_file) as foo:
        lines = len(foo.readlines())
    foo.close()
    return (lines)

###############
def get_info_file(input_file):    
    with open(input_file) as f:
        lines = f.read().splitlines() 
    f.close()
    return (lines)
          
#################
def optimize_threads(total, samples):
    cpu = int(int(total)/int(samples))
    
    if (cpu==0): ## 5 availabe cpus for 10 samples == 0 cpu
        cpu = 1
    
    return(cpu)

#################
def parse_sublist(lst, ind): 
    ## extract elemnts of the list
    ## Original Code: https://www.geeksforgeeks.org/python-get-first-element-of-each-sublist/
    return [item[ind] for item in lst]

##################
def decode(x):
    """
    Python decode string method

    It converts bytes to string.

    :param x: String of text to decode
    :type x: string
    :returns: Text decoded

    .. attention:: Be aware of Copyright

        The code implemented here was retrieved and modified from ARIBA (https://github.com/sanger-pathogens/ariba)

        Give them credit accordingly.
    """
    try:
        s = x.decode()
        return s
    except:
        return x

