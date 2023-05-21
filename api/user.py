from api.Connect import connect
from api.xuli import *
import pyodbc

def checkLogin(rq):    
    rs={}
    print(list(rq))
    if(not checkInvalid(rq,['username','password'])):
        rs={
            'status': 'error',
            'mess' : 'data invalid'
        }
        
    elif(not checkNull(rq,['username','password'])):
        rs={
            'status': 'error',
            'mess' : 'data null'
        }
        
    else:
        username=rq['username']
        password=rq['password']
        conn = connect()
        cursor = conn.cursor        
        sql=f"select * from TaiKhoan where taiKhoan='{username}'"        
        cursor.execute(sql)
        record = cursor.fetchone()
        if record is None:
            rs = {
                'status': 'error',
                'mess' : 'Sai thông tin đăng nhập'
            }
        elif record[2]!=password:
            rs = {
                'status': 'error',
                'mess' : 'Sai thông tin đăng nhập',    
            }
        else:
            rs = {
                'status': 'success',
                'data':{
                    "maTaiKhoan":record.maTaiKhoan,
                    "taiKhoan":record.taiKhoan,
                    "phanQuyen":record.phanQuyen,
                    "trangThai":record.trangThai,
                    "hoTen":record.hoTen,
                    "ngaySinh":formatDate(record.ngaySinh),
                    "cccd":record.cccd,
                    "sdt":record.sdt,
                    "diaChi":record.diaChi,
                    "gioiTinh":record.gioiTinh,
                    "avatar":record.avatar
                }                
            }
        conn.close()   
    return rs

def addAccount(rq):
    rs={}
    if(not checkInvalid(rq,['username','password','role'])):
        rs={
            'status': 'error',
            'mess' : 'data invalid'
        }
        
    elif(not checkNull(rq,['username','password','role'])):
        rs={
            'status': 'error',
            'mess' : 'data null'
        }
    elif(rq['role'] not in ['Khách hàng','Nhân viên']):
        rs={
            'status': 'error',
            'mess' : 'role invalid'
        }
    else:
        taiKhoan=rq['username']
        password=rq['password']
        role=rq['role']
        conn = connect()
        cursor = conn.cursor
        connection= conn.connection
        sql=f"SELECT * From TaiKhoan Where taiKhoan='{taiKhoan}'"
        cursor.execute(sql)
        rows = cursor.fetchone()
       
        if(rows):
            rs={
                'status': 'error',
                'mess' : 'Tài khoản đã tồn tại'
            }
        else:
            try:
                cursor.execute("SET DATEFORMAT dmy")
                cursor.execute("EXEC pr_add_account @taiKhoan=?, @matKhau=?, @phanQuyen=?",taiKhoan,password,role)
                connection.commit()
                rs={
                    'status':'success'
                }
            except pyodbc.Error as ex:
                rs={
                    'status': 'error',
                    'mess' : ex
                }
                print(ex)
        conn.close()
    return rs

def changePass(rq):
    rs={}
    if(not checkInvalid(rq,['username','newPassword','oldPassword'])):
        rs={
            'status': 'error',
            'mess' : 'data invalid'
        }
        
    elif(not checkNull(rq,['username','newPassword','oldPassword'])):
        rs={
            'status': 'error',
            'mess' : 'data null'
        }
    elif rq['newPassword']==rq['oldPassword']:
        rs={
            'status': 'error',
            'mess' : "new password can not be old password"
        }
    else:
        username=rq['username']
        newPassword=rq['newPassword']
        oldPassword=rq['oldPassword']

        conn = connect()
        cursor = conn.cursor
        connection= conn.connection
        sql=f"SELECT * FROM TaiKhoan WHERE taiKhoan='{username}'"
        cursor.execute(sql)
        row= cursor.fetchone()
        if not row:
            rs={
                'status': 'error',
                'mess': 'Account is not exits'
            }
        elif oldPassword!=row.matKhau:
            rs={
                'status':'error',
                'mess':'Old pass is not correct'
            }
        else:
            try:
                
                sql="UPDATE TaiKhoan SET matKhau = ? WHERE taiKhoan=?"
                cursor.execute(sql,newPassword,username)
                cursor.commit()
                rs={
                    'status':'success',
                    'mess':'Change pass success'
                }
            except pyodbc as ex:
                rs={
                    'status':'error',
                    'mess': str(ex)
                }
                print(ex)
        conn.close()
    return rs

# def updateInfoUser(rq):


