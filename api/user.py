from api.Connect import connect
from api.xuli import *
import pyodbc
from pathlib import Path

ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'

def checkLogin(rq):    
    rs={}
    print(list(rq))
    if(not checkInvalid(rq,['username','password'])):
        rs=printRs(ERROR,DATA_INVALID,None)
        
    elif(not checkNull(rq,['username','password'])):
        rs=printRs(ERROR,DATA_NULL,None)
    else:
        username=rq['username']
        password=rq['password']
        conn = connect()
        cursor = conn.cursor        
        sql=f"select * from TaiKhoan where taiKhoan='{username}'"        
        cursor.execute(sql)
        record = cursor.fetchone()        
        if record is None:
            rs = printRs(ERROR,'Sai tài khoản',None)
        elif record.matKhau!=password:
            rs = printRs(ERROR,'Sai mật khẩu',None)
        else:
            columnName=[column[0] for column in cursor.description]
            rs = printRs(SUCCESS,None,rsData([record],columnName))
        conn.close()   
    return rs

def addAccount(rq):
    rs={}
    if(not checkInvalid(rq,['username','password','role'])):
        rs=printRs(ERROR,DATA_INVALID,None)
        
    elif(not checkNull(rq,['username','password','role'])):
        rs=printRs(ERROR,DATA_NULL,None)
    elif(rq['role'] not in ['Khách hàng','Nhân viên']):
        rs=printRs(ERROR,'Role invalid',None)
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
            rs=printRs(ERROR,'Tài khoản đã tồn tại',None)
        else:
            try:
                cursor.execute("SET DATEFORMAT dmy")
                cursor.execute("EXEC pr_add_account @taiKhoan=?, @matKhau=?, @phanQuyen=?",taiKhoan,password,role)
                connection.commit()
                rs=printRs(SUCCESS,None,None)
            except pyodbc.Error as ex:
                rs=printRs(ERROR,str(ex),None)
        conn.close()
    return rs

def changePass(rq):
    rs={}
    if(not checkInvalid(rq,['maTaiKhoan','newPassword','oldPassword'])):
        rs=printRs(ERROR,DATA_INVALID,None)        
    elif(not checkNull(rq,['maTaiKhoan','newPassword','oldPassword'])):
        rs=printRs(ERROR,DATA_NULL,None)
    elif rq['newPassword']==rq['oldPassword']:
        rs=printRs(ERROR,'New password can not be old password',None)
    else:
        maTaiKhoan=rq['maTaiKhoan']
        newPassword=rq['newPassword']
        oldPassword=rq['oldPassword']

        conn = connect()
        cursor = conn.cursor
        sql=f"SELECT * FROM TaiKhoan WHERE maTaiKhoan='{maTaiKhoan}'"
        cursor.execute(sql)
        row= cursor.fetchone()
        if not row:
            rs=printRs(ERROR,'Tài khoản không tồn tại',None)
        elif oldPassword!=row.matKhau:
            rs=printRs(ERROR,'Mật khẩu cũ không chính xác',None)
        else:
            try:
                
                sql="UPDATE TaiKhoan SET matKhau = ? WHERE maTaiKhoan=?"
                cursor.execute(sql,newPassword,maTaiKhoan)
                cursor.commit()
                rs=printRs(SUCCESS,'Đổi mật khẩu thành công',None)
            except pyodbc as ex:
                rs=printRs(ERROR,str(ex),None)
                print(ex)
        conn.close()
    return rs

async def updateInfoUser(rq,relative_path):
    rs={}
    listParamsAccept=['maTaiKhoan','email','hoTen','ngaySinh','cccd','sdt','diaChi','gioiTinh','avatar']
    listParams=list(rq.keys())
    
    if not checkParmasRq(listParams,listParamsAccept):
        rs=printRs(ERROR,DATA_INVALID,None)
        
    else:
        conn = connect()
        cursor = conn.cursor
        connection= conn.connection
        sql=f"SELECT * FROM TaiKhoan WHERE maTaiKhoan='{rq['maTaiKhoan']}'"
        cursor.execute(sql)
        row=cursor.fetchone()
        if not row:
            rs=printRs(ERROR,'Mã tài khoản sai',None)
        else:
            try:
                paramsUpdate=[param for param in listParams if param not in ['maTaiKhoan','avatar']]
                sql=f"UPDATE TaiKhoan SET {getStringSQL(paramsUpdate)} WHERE maTaiKhoan='{rq['maTaiKhoan']}'"
                new_values=[rq[value] for value in paramsUpdate]
                cursor.execute('SET DATEFORMAT dmy')
                cursor.execute(sql,new_values)
                
                rs=printRs(SUCCESS,'Đổi thông tin thành công',None)
                
                if 'avatar' in listParams and not isinstance(rq['avatar'],str):
                    deleteImg(relative_path,row.avatar)
                    duoiFile=Path(rq['avatar'].filename).suffix
                    tenFile=rq['maTaiKhoan']+duoiFile
                    save_path = f"{relative_path}\{tenFile}"
                    print(save_path)
                    print(relative_path)
                    with open(save_path, "wb") as file:
                        file.write(await rq['avatar'].read())
                    cursor.execute(f"UPDATE TaiKhoan SET avatar='{tenFile}' WHERE maTaiKhoan='{rq['maTaiKhoan']}'")
                cursor.commit()
            except pyodbc as ex:
                print(ex)
                rs=printRs(ERROR,str(ex),None)     
            except :
                rs=printRs(ERROR,"Lỗi chưa xác định",None)          
        conn.close()
    return rs


    


