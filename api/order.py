from api.Connect import connect
from api.xuli import *
import pyodbc
from pathlib import Path
from datetime import date


ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'

def getAllOrder(page,q=None,maTaiKhoan=None):
    so_item=10
    vt=(page-1)*so_item

    # kt=(page-1)*10+10
    conn = connect()
    cursor = conn.cursor 
    rs={}
    strSearch=""
    if q is not None:     
        strSearch+=f" WHERE maTaiKhoan LIKE '%{q}%'' or maThue LIKE '%{q}%''"
    sql=f"SELECT * from DangKyThueXe "+strSearch +f" order by ngayBD desc OFFSET {vt} ROWS FETCH NEXT {so_item} ROWS ONLY;"
    cursor.execute(sql)
    data_don = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_don=rsData(data_don,columnName)
    

    sql="SELECT ChiTietThueXe.*,tenXe,loaiXe,hangXe,bienSoXe from ChiTietThueXe,Xe where ChiTietThueXe.maXe=Xe.maXe"
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
    print(new_data_chitiet)
    
    new_data=mergeData(data_don,new_data_chitiet,"maThue","chiTiet")

    sql=f"SELECT count(maThue) as soLuong from DangKyThueXe "+strSearch
    cursor.execute(sql)
    row = cursor.fetchone()
    soLuong=row[0]
    rs = printRs(SUCCESS,None,new_data)
    rs['soTrang']=getSoTrang(soLuong,so_item)
    conn.close()
    return rs

def getOrder(id_order):
    
    # kt=(page-1)*10+10
    conn = connect()
    cursor = conn.cursor 
    rs={}
    
    sql=f"SELECT * from DangKyThueXe where maThue='{id_order}'"
    
    
    cursor.execute(sql)
    data_don = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_don=rsData(data_don,columnName)

    
    
    sql=f"SELECT ChiTietThueXe.*,tenXe,loaiXe,hangXe,bienSoXe from ChiTietThueXe,Xe where ChiTietThueXe.maXe=Xe.maXe and ChiTietThueXe.maThue='{data_don[0]['maThue']}'"
    cursor.execute(sql)
    data_chitiet = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_chitiet=rsData(data_chitiet,columnName)

    sql=f"SELECT ct.maLoi as maLoi,lp.noiDungLoi as noiDungLoi,ct.ghiChu as ghiChu,ct.tienPhat as tienPhat FROM ChiTietLoiPhat as ct, LoiPhat as lp WHERE ct.maLoaiLoi = lp.maLoaiLoi and ct.maLoi='{data_chitiet[0]['maLoi']}'"
    cursor.execute(sql)
    data_loi = cursor.fetchall()
    columnName=[column[0] for column in cursor.description]
    data_loi=rsData(data_loi,columnName)
    
    new_data_chitiet=mergeData(data_chitiet,data_loi,"maLoi","loi")
    new_data=mergeData(data_don,new_data_chitiet,"maThue","chiTiet")

    
    
    rs = printRs(SUCCESS,None,new_data)
   
    conn.close()
    return rs

def nvSetOrder(rq):
    paramsAcceep=['maNVDuyet','maThue','trangThai']
    
    rs={}
    if not checkInvalid(rq,paramsAcceep):
        rs = printRs(ERROR,DATA_INVALID,None)
    elif not checkNull(rq,paramsAcceep):
        rs = printRs(ERROR,DATA_INVALID,None)
    else:
        conn = connect()
        cursor = conn.cursor 
        # try:
        sql=f"SELECT * from TaiKhoan WHERE maTaiKhoan='{rq['maNVDuyet']}'" 
        cursor.execute(sql)
        row = cursor.fetchone
        if not row:
            rs = printRs(ERROR,"Mã nhân viên không tồn tại",None)
        else:
            sql=f"SELECT * from DangKyThueXe WHERE maThue='{rq['maThue']}'"
            cursor.execute(sql)
            row = cursor.fetchone()
            
            
            stringGhiChu= row.ghiChu if row.ghiChu is not None else " "
 
            stringGhiChu+= rq['maNVDuyet'] + "  " + rq['trangThai'] + f"  ngày :{str(getDateNow())}; "
     
            if not row:
                rs = printRs(ERROR,"Mã thuê không tồn tại",None)
            else:
                new_value=[rq['trangThai'],stringGhiChu,str(getDateNow())]
                stringSQL=""
                if rq['trangThai']=='Đã duyệt':
                    stringSQL=f",maNVDuyet=?"
                    new_value.append(rq['maNVDuyet'])
                new_value.append(rq['maThue'])
                sql="UPDATE DangKyThueXe SET trangThai=?,ghiChu=?,ngayDuyet=?"+stringSQL+" WHERE maThue=?"
                cursor.execute('SET DATEFORMAT dmy')
                cursor.execute(sql,new_value)
                cursor.commit()
                rs= printRs(SUCCESS,"Set trạng thái thành công",None)
        # except:
        #     rs = printRs(ERROR,"Lỗi không xác định",None)
        conn.close()
    return rs

def addOrder(rq):
    rs={}    
    paramsAcess=['maKH','ngayBD','ngayKT','listMoto']
    if not checkInvalid(rq,paramsAcess):
        print(DATA_INVALID)
        rs=printRs(ERROR,DATA_INVALID,None)
    if not checkNull(rq,rq):
        print(DATA_NULL)
        rs = printRs(ERROR,DATA_NULL,None)
    else:
        conn = connect()
        cursor = conn.cursor
        sql=f"EXEC pr_getFreeMoto @ngayBD=?,@ngayKT=?"
        cursor.execute('SET DATEFORMAT dmy')
        cursor.execute(sql,[rq['ngayBD'],rq['ngayKT']])
        rows = cursor.fetchall()
        # for car in rq['listMoto']:
        #     if car
        new_rows = [row[0] for row in rows]
        
        xe_not_correct=set(rq['listMoto']) - set(new_rows)
        if len(xe_not_correct)!=0:
            rs= printRs(ERROR,"Xe đã được đặt thuê",list(xe_not_correct))
        else:
            
            sql="{CALL pr_add_dangKyThueXe(?, ?, ?, ?)}"
            cursor.execute("SET DATEFORMAT dmy")
            cursor.execute(sql, (rq['maKH'],rq['ngayBD'],rq['ngayKT'],'-'.join(rq['listMoto'])))
            cursor.commit()
            rs = printRs(SUCCESS,"Thêm đơn hàng thành công",None)
        conn.close()
    return rs

def payOrder(rq):
    rs={}    
    paramsAcess=['maThue','xe','maNVNhanXe']
    if not checkInvalid(rq,paramsAcess):
        rs = printRs(ERROR,DATA_INVALID,None)
    elif not checkNull(rq,rq):
        rs = printRs(ERROR,DATA_NULL,None)
    else:
        conn = connect()
        cursor = conn.cursor
        if conn.dataNotExist('DangKyThueXe','maThue',rq['maThue']):
            rs= printRs(ERROR,"Mã thuê không tồn tại",None)
        elif conn.dataNotExist('TaiKhoan','maTaiKhoan',rq['maNVNhanXe']):
            rs= printRs(ERROR,"Mã nhân viên không tồn tại",None)
        else:
            
            for xe in rq['xe']:
                #Update Chi tiet thue xe
                cursor.execute("SET DATEFORMAT dmy")
                sql=f"UPDATE ChiTietThueXe SET ngayTra=?,maNVNhanXe=? WHERE maThue=? and maXe=?"
                new_value=[getDateNow(),rq['maNVNhanXe'],rq['maThue'],xe['maXe']]
                cursor.execute(sql,new_value)

                #Update lỗi xe
                sql=f"INSERT INTO ChiTietLoiPhat (maLoi, maLoaiLoi,ghiChu,tienPhat) VALUES (?,?,?,?)"
                new_value_loi=[]
                for loi in xe['loi']:
                    txtGhiChu=''
                    if 'ghiChu' in loi:
                        txtGhiChu=loi['ghiChu']
                    new_value_loi_item=(xe['maLoi'],loi['maLoaiLoi'],txtGhiChu,loi['tienPhat'])
                    new_value_loi.append(new_value_loi_item)
                if(len(new_value_loi)!=0):
                    cursor.executemany(sql,new_value_loi)
            rs = printRs(SUCCESS,"Thanh toán hoàn tất",None)
            cursor.commit()
        conn.close()
    return rs

