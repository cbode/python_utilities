# -*- coding: utf-8 -*-
#!/usr/bin/python3
################################################################################
# name: utilities_file.py
# author: collin bode, email: collin@berkeley.edu
# created date: 2016-08-01
#
# purpose: Functions for the manipulation of files and pathnames
################################################################################

import os

def get_filepath():
    # Get absolute path to this file
    path = os.path.dirname(__file__)
    path = path+os.sep
    return path
