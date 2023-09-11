from api.Connect import connect
from api.xuli import *
import pyodbc
from pathlib import Path
from api.FireBase import *
from io import BytesIO
ERROR='error'
SUCCESS='success'
DATA_INVALID='Data invalid'
DATA_NULL='Data null'


async def addXe(rq,relative_path,files):
    rs={}
    paramsAccept=['tenXe','hangXe','bienSoXe','loaiXe','giaThue','trangThai','moTa','images']
    listParams=list(rq.keys())

    
    if not checkInvalid(listParams,paramsAccept):
        rs= printRs(ERROR,DATA_INVALID,None)
    elif not checkNull(rq,paramsAccept[:-2]):
        rs= printRs(ERROR,DATA_NULL,None)
    else:
        conn = connect()
        cursor = conn.cursor
        connection= conn.connection
        # try:          
        sql=f"SELECT * from Xe where bienSoXe='{rq['bienSoXe']}'"
        
        cursor.execute(sql)
        row = cursor.fetchone()
                 
        if row:
            rs= printRs(ERROR,"Biển số xe đã tồn tại",None)
        else:    
            strListHinhAnh=''
            i=0
            uploaded_urls = []
            connector = FirebaseConnector()
            if files is not None:
                for x in files:
                    duoiFile=Path(x.filename).suffix
                    tenFile=createNameImgXe(rq['tenXe'],rq['bienSoXe'])+"-"+str(i)+duoiFile
                    # save_path = f"{relative_path}\{tenFile}"
                    image_data = BytesIO(await x.read())
                    
                    image_url = connector.upload_image(image_data,tenFile)
                    uploaded_urls.append(image_url)
                    i+=1
                    print(i)

            print(uploaded_urls)
            # strListHinhAnh=strListHinhAnh.rstrip(";")
            # cursor.execute("SET DATEFORMAT dmy")
            # params=[rq['tenXe'],rq['hangXe'],rq['trangThai'],rq['bienSoXe'],rq['loaiXe'],rq['giaThue'],rq['moTa']]
            # sql="EXEC pr_add_Xe @tenXe=?,@hangXe=?,@trangThai=?,@bienSoXe=?,@loaiXe=?,@giaThue=?,@moTa=?"
            # if strListHinhAnh!='':
            #     sql+=",@listHinhAnh=?"
            #     params.append(strListHinhAnh)
        
            
            # cursor.execute(sql,params)
            # cursor.commit()
            rs=printRs(SUCCESS,"Thêm xe thành công",None)
        # except pyodbc.Error as ex:
        #     print(ex)
        #     rs=printRs(ERROR,"Lỗi SQL",None)
        # except:
        #     print("loi")
        #     rs=print(ERROR,"Lỗi không xác định",None)        
        conn.close()
    return rs
