from api.Connect import connect
from api.xuli import *
import pyodbc
from pathlib import Path

ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'

def getAllOrder(q):
    conn = connect()
    cursor = conn.cursor 
    rs={}
    strSearch=""
    if q is not None:     
        strSearch+=f" WHERE maTaiKhoan LIKE '%{q}%''"
    sql="SELECT * from DangKyThueXe "+strSearch+" order by maThue"
    cursor.execute(sql)
    data_don = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_don=rsData(data_don,columnName)


    sql="SELECT * from ChiTietThueXe"+" order by maThue"
    cursor.execute(sql)
    data_chitiet = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_chitiet=rsData(data_chitiet,columnName)

    sql="SELECT ct.maLoi as maLoi,lp.noiDungLoi as noiDungLoi,ct.ghiChu as ghiChu,ct.tienPhat as tienPhat FROM ChiTietLoiPhat as ct, LoiPhat as lp WHERE ct.maLoaiLoi = lp.maLoaiLoi"
    cursor.execute(sql)
    data_loi = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_loi=rsData(data_loi,columnName)
    
    new_data_chitiet=mergeData(data_chitiet,data_loi,"maLoi","loi")
    new_data=mergeData(data_don,new_data_chitiet,"maThue","chiTiet")

    conn.close()
    return new_data


def nvSetOrder(rq):
    paramsAcceep=['maNVDuyet','maThue','trangThai']

