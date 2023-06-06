from api.Connect import connect
from api.xuli import *
import pyodbc
import os

ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'

def getALlLoi():
    conn = connect()
    cursor = conn.cursor
    
    sql='Select * from LoiPhat'
    cursor.execute(sql)
    rows= cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    
    return printRs(SUCCESS,None,rsData(rows,columnName))

