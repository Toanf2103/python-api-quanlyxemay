from api.Connect import connect
from api.xuli import *
import pyodbc

ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'

def getAllXe():
    conn = connect()
    cursor = conn.cursor
    rs = {}
    sql='SELECT * FROM Xe'
    cursor.execute(sql)
    rows = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    dataXe=rsData(rows,columnName)
    sql='SELECT * from HinhAnhXe'
    cursor.execute(sql)
    dataHinhAnh=cursor.fetchall()
    for xe in dataXe:
        xe['hinhAnh']=[]
        hinh_anh_list = []
        for hinhAnh in dataHinhAnh:
            if xe['maXe']==hinhAnh.maXe:
                hinh_anh_list.append(getURLImg('hinhAnh',hinhAnh.hinhAnh))
        xe['hinhAnh']=hinh_anh_list
    rs = printRs(SUCCESS,None,dataXe)
    conn.close()
    return rs

def addXe(tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue):
    rs={}
    conn = connect()
    cursor = conn.cursor
    connection= conn.connection
    try:
        cursor.execute("{CALL pr_add_Xe(?, ?, ?, ?, ?, ?)}", (tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue))
        connection.commit()        
        rs=printRs(SUCCESS,"Thêm xe thành công",None)
    except pyodbc.Error as ex:
        rs=printRs(ERROR,"Lỗi SQL",None)
    except:
        rs=print(ERROR,"Lỗi không xác định",None)
    conn.close()
    return rs