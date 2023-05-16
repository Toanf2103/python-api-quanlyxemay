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

def checkLogin(username,password):
    
    # rs={}
    # if('username' not in rq or 'password' not in rq):
    #     rs={
    #         'status': 'error',
    #         'mess' : 'data invalid'
    #     }
    # elif(not rq['username'] or not rq['password']):
    #     rs={
    #         'status': 'error',
    #         'mess' : 'data invalid'
    #     }
    # else:
    #     username=rq['username']
    #     password=rq['password']
    #     conn = connect()
    #     cursor = conn.cursor
        
    #     sql=f"select * from TaiKhoan where taiKhoan='{username}'"
        
    #     cursor.execute(sql)
    #     record = cursor.fetchone()
    #     if record is None:
    #         rs = {
    #             'status': 'error',
    #             'mess' : 'Sai thông tin đăng nhập'
    #         }
    #     elif record[2]!=password:
    #         rs = {
    #             'status': 'error',
    #             'mess' : 'Sai thông tin đăng nhập',    
    #         }
    #     else:
    #         rs = {
    #             'status': 'success',
    #             'data':{
    #                 "maTaiKhoan":record[0],
    #                 "taiKhoan":record[1],
    #                 "phanQuyen":record[3],
    #                 "trangThai":record[4],
    #                 "hoTen":record[5],
    #                 "ngaySinh":record[6],
    #                 "cccd":record[7],
    #                 "sdt":record[8],
    #                 "diaChi":record[9],
    #                 "gioiTinh":record[10],
    #                 "avatar":record[11]
    #             }
                
    #         }
    #     conn.close()
    return {
        'username':username,
        'pass':password
    }
def getDonHang():
    conn = connect()
    cursor = conn.cursor
    
    sql='select ngayBD from DangKyThueXe'
    cursor.execute("SET DATEFORMAT dmy")
    cursor.execute(sql)
    rows= cursor.fetchall()
    data=[]
    for item in rows:
        data.append({'ngayBD':formatDate(item.ngayBD)})
    return data
def addDonHang(maKH,ngayBD,ngayKT,listCar):
    conn = connect()
    cursor = conn.cursor
    connection= conn.connection
    
    try:
        cursor.execute("SET DATEFORMAT dmy")
        cursor.execute("{CALL pr_add_dangKyThueXe(?, ?, ?, ?)}", (maKH,ngayBD,ngayKT,listCar))
        connection.commit()
        conn.close()
        return {
            'stt':True
        }
    except pyodbc.Error as ex:
        return {
            'stt':False,
            'ms':ex
        }

def test(listCar):
    # print(type(listCar))
    for x in listCar:
        print(x)
    return {
        'type':'cac'
    }

