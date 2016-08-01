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
    
# Configuration
fpath = '/Users/cbode/Documents/WorkSync/UCNRS/DRI/ucac_dri.dat'
delim = ','

# Determine how many rows of header
fin = open(fpath,'r')
i = 0
for row in fin:
    fields = row.split(delim)
    if(is_datetime(fields[0]) == True):
        print('HEADER is ',i,' rows long')
        break
    elif(i > 100): 
        print('Datetime not found. Quitting.')
        break
    else:
        i += 1
        print(fields[0],' is not a time')
fin.close()
header_length = i

# Import values into DataFrame sort and analyze
df = pd.read_csv(fpath,sep=delim,header=None,skiprows=header_length,parse_dates=0)

