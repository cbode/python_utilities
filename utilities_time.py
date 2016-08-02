# -*- coding: utf-8 -*-
#!/usr/bin/python3
################################################################################
# name: utilities.py
# author: collin bode, email: collin@berkeley.edu
# date: 2016-05-09
#
# purpose: Functions for the manipulation of timeseries data and files.
################################################################################

import os
import datetime as dt
import pandas as pd

# Get absolute path to this file
def get_filepath():
    path = os.path.dirname(__file__)
    path = path+os.sep
    return path
    
# Determine if text is a timestamp without crashing
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

# Determine how many rows in the header
def get_header_row_length(fpath,delim,verbose):
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

# Opens timeseries file and creates Pandas DataFrame
def create_timeseries_dataframe(fpath,delim,date_as_index):
    header_length = get_header_row_length(fpath,delim,False)
    if(date_as_index == True):
        df = pd.read_csv(fpath,sep=delim,header=None,prefix='c',skiprows=header_length,parse_dates=0, date_parser=pd.datetools.datetime,index_col=0)        
    else:
        df = pd.read_csv(fpath,sep=delim,header=None,prefix='c',skiprows=header_length,parse_dates=0, date_parser=pd.datetools.datetime,dtype={0:dt.datetime},low_memory=False)
    return df

def get_duplicate_timestamp_count(df):
    df['dup'] = df.duplicated(subset='c0')
    return df['dup'].sum()    

def return_duplicate_timestamps(df,both,allfields):
    # both = True.  Return both the original and the duplicate row.
    # both = False means you just return the second or more rows, not the original.
    # allfields = True means every field will be compared to determine duplicate.  This will leave duplicate timestamps if the fields are different.
    # allfields = False means only the timestamp will be considered.
    if(both == True and allfields == True):
        df['dup'] = df.duplicated(subset='c0',keep=False)
    elif(both == True and allfields == False):
        df['dup'] = df.duplicated(keep=False)
    elif(both == False and allfields == True):
        df['dup'] = df.duplicated(subset='c0')    
    else:
        df['dup'] = df.duplicated()
    dups = df[df['dup'] == True]
    return dups
    
def remove_duplicate_timestamps(df,allfields):
    # allfields = False means only the timestamp will be considered when removing duplicates.
    # allfields = True means every field will be compared to determine duplicate.  This will leave duplicate timestamps if the fields are different.
    if(allfields == False):
        df['dup'] = df.duplicated(subset='c0')
    else:
        df['dup'] = df.duplicated()
    dfclean = df.drop(df[df.dup == True].index)
    return dfclean

def check_timeseries_gaps(df,interval):
    # interval should be in minutes, e.g. '10Min'
    # note: requires no duplicate timestamps
    dfclean = remove_duplicate_timestamps(df,True)
    dfclean.set_index('c0',inplace=True)    
    mindate = dfclean.index.min()        
    maxdate = dfclean.index.max()
    ti = pd.date_range(start=mindate,end=maxdate,freq=interval)
    
    
################################    
# Main runs test cases

# Configuration
path = get_filepath()
datfile = 'dup_test.dat'
fpath = path+datfile
delim = ','
df = create_timeseries_dataframe(fpath,delim,False)

'''
# Find out how many rows there are in the header
header_length = get_header_row_length(fpath,delim,True)
print('Header is ',header_length,' rows long')

# Check file for duplicates
number_dups = get_duplicate_timestamp_count(fpath,delim)
print('Number of duplicate timestamps: ',number_dups)

# List all duplicate timestamps 
dups = return_duplicate_timestamps(fpath,delim,True,True)
print('All timestamps that are duplicate.  Will return rows with different other fields, if timestamp is the same.')
print(dups)

# List all perfectly duplicated rows 
dups = return_duplicate_timestamps(fpath,delim,False,True)
print('Rows that are duplicate in all fields.')
print(dups)

# Delete Duplicates from dataset 
dfclean = remove_duplicate_timestamps(path,delim,False)
print(dfclean)
'''

# Check Timeseries for gaps
