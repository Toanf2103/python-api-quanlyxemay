from api.Connect import connect
from api.xuli import *
import pyodbc

def getAllXe():
    conn = connect()
    cursor = conn.cursor
    data = []
    sql='SELECT maXe,tenXe,hangXe,bienSoXe,loaiXe,giaThue,trangThai FROM Xe'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        xe = {"maXe": row.maXe, "tenXe": row.tenXe, "hangXe": row.hangXe, "bienSoXe": row.bienSoXe, "loaiXe": row.loaiXe, "giaThue": row.trangThai, "trangThai": row.bienSoXe}
        data.append(xe)
    conn.close()
    return data

def addXe(tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue):
    conn = connect()
    cursor = conn.cursor
    connection= conn.connection
    try:
        
        cursor.execute("{CALL pr_add_Xe(?, ?, ?, ?, ?, ?)}", (tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue))
        connection.commit()
        conn.close()
        
        return {
            'status': 'success'
        }
    except pyodbc.Error as ex:
        conn.close()
        return  {
            'status': 'error',
            'mess' : 'add fail'
        }