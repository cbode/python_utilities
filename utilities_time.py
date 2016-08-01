# -*- coding: utf-8 -*-
#!/usr/bin/python3
################################################################################
# name: utilities_time.py
# author: collin bode, email: collin@berkeley.edu
# date: 2016-05-09
#  added to github
# purpose: Functions for the manipulation of timeseries data
################################################################################

import os
import datetime as dt
import pandas as pd
from utilities_file import get_filepath

def is_datetime(dtstring):
    if dtstring.startswith('"') and dtstring.endswith('"'):
        dtstring = dtstring[1:-1]
    if dtstring.startswith("'") and dtstring.endswith("'"):
        dtstring = dtstring[1:-1]
    try:
        timestamp = dt.datetime.strptime(dtstring,"%Y-%m-%d %H:%M:%S")
        return True        
    except:
        return False

def get_header_row_length(path,delim,verbose):
    # Determine how many rows of header
    fin = open(fpath,'r')
    i = 0
    for row in fin:
        fields = row.split(delim)
        if(is_datetime(fields[0]) == True):
            if(verbose == True): print('HEADER is ',i,' rows long')
            break
        elif(i > 100): 
            if(verbose == True): print('Datetime not found. Quitting.')
            break
        else:
            i += 1
            if(verbose == True): print(fields[0],' is not a time')
    fin.close()
    return i

def get_duplicate_timestamp_count(path,delim):
    header_length = get_header_row_length(path,delim,False)
    df = pd.read_csv(fpath,sep=delim,header=None,prefix='c',skiprows=header_length,parse_dates=[0])
    df['dup'] = df.duplicated(subset='c0')
    return df['dup'].sum()    

def return_duplicate_timestamps(path,delim,both):
    # both = True.  Return both the original and the duplicate row.
    # both = False means you just return the second or more rows, not the original.
    header_length = get_header_row_length(path,delim,False)
    df = pd.read_csv(fpath,sep=delim,header=None,prefix='c',skiprows=header_length,parse_dates=[0])
    if(both == True):
        #dupsplus = pd.merge(dups,df,how='left',left_on='c0',right_on='c0')
        df['dup'] = df.duplicated(subset='c0',keep=False)
    else:
        df['dup'] = df.duplicated(subset='c0')
    dups = df[df['dup'] == True]
    return dups
    
def remove_duplicate_timestamps(path,delim,allfields):
    # allfields = False means only the timestamp will be considered when removing duplicates.
    # allfields = True means every field will be compared to determine duplicate.  This will leave duplicate timestamps if the fields are different.
    header_length = get_header_row_length(path,delim,False)
    df = pd.read_csv(fpath,sep=delim,header=None,prefix='c',skiprows=header_length,parse_dates=[0])
    if(allfields == False):
        df['dup'] = df.duplicated(subset='c0')
    else:
        df['dup'] = df.duplicated()
    dfclean = df.drop(df[df.dup == True].index)
    return dfclean


################################    
# Main runs test cases

# Configuration
path = get_filepath()
datfile = 'dup_test.dat'
fpath = path+datfile
delim = ','

# Find out how many rows there are in the header
header_length = get_header_row_length(fpath,delim,True)
print('Header is ',header_length,' rows long')

# Check file for duplicates
number_dups = get_duplicate_timestamp_count(fpath,delim)
print('Number of duplicate timestamps: ',number_dups)

# List all duplicate timestamps 
dups = return_duplicate_timestamps(fpath,delim,True)
print('All timestamps that are duplicate.  Will return rows with different other fields, if timestamp is the same.')
print(dups)

# List all perfectly duplicated rows 
dups = return_duplicate_timestamps(fpath,delim,False)
print('Rows that are duplicate in all fields.')
print(dups)

# Delete Duplicates from dataset 
dfclean = remove_duplicate_timestamps(path,delim,False)
