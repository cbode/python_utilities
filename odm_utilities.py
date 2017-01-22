# -*- coding: utf-8 -*-
#!/usr/bin/python3
################################################################################
# name: odm_utilities.py
# author: collin bode, email: collin@berkeley.edu
# date: 2017-01-21
#
# purpose: Sensor Database ODM mysql access.
# Note: gall can only be accessed from campus or using VPN
# pwfilepath: text file with username on first line, password on second line
# no other text.
################################################################################
import pandas as pd
import mysql.connector
import datetime as dt

def odm_connect(pwfilepath,boo_dev=False):
    # NOTE: password file (pwfile) should NEVER be uploaded to github!
    fpw = open(pwfilepath,'r')
    user = fpw.readline().strip()
    pw = fpw.readline().strip()
    fpw.close()
    if(boo_dev == True):
        db = 'odm_dev'
    else:
        db = 'odm'
    cnx = mysql.connector.connect(
        user=user,
        password=pw,
        host='gall.berkeley.edu',
        database=db)
    return cnx

def odmquery(conn,datestart,dateend,dsid):
    # NOTE: this excludes bad data. To include bad data, remove Qualifier sql    
    # Construct SQL query
    sql = 'SELECT DV.LocalDateTime, DV.DataValue ' + \
    'FROM datavalues2 DV, qualifiers Q ' + \
    'WHERE DV.LocalDateTime >= "'+datestart+'" AND ' + \
    'DV.LocalDateTime <= "'+dateend+'" AND '+ \
    '(DV.DatastreamID = "'+dsid+'" AND DV.QualifierID = Q.QualifierID) AND' + \
    '(Q.QualifierCode not like "X%") '
    'ORDER BY DV.LocalDateTime'

    # Pull data from odm sensor database into Pandas Dataframe
    df = pd.read_sql_query(sql,con=conn)

    # Set Datetime as index
    df.set_index(['LocalDateTime'],inplace=True)
    return df


# test functions 
conn = odm_connect('odm.pw')
datestart = '2014-012-04 12:00:00'
dateend = '2015-01-10 00:00:00'
dsid = '2'
df = odmquery(conn,datestart,dateend,dsid)
print(df)
conn.close()