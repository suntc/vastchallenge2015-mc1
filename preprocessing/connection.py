'''
Created on 2016-1-4

@author: sun tianchen
'''

import MySQLdb

def connection():
    conn=MySQLdb.connect(host='localhost',user='sun',passwd='sun123456')
    cur=conn.cursor()
    cur.execute("use dinoworld")
    return conn,cur