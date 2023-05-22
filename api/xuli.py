from datetime import datetime
import os
from unidecode import unidecode
import re
def formatDate(ngay):
    formatType="%d-%m-%Y"
    return ngay.strftime(formatType)

def checkInvalid(rq,params):
    for param in params:
        if param not in rq:
            return False
    return True
def checkNull(rq,params):
    for param in params:
        if rq[param] is None:
            return False
    return True
def checkParmasRq(rq,params):
    for x in rq:
        if x not in params:
            return False
    return True
def is_empty_upload_file(upload_file):
    if upload_file.file is None or upload_file.filename == "":
        return True
    return False

def getStringSQL(params,char):
    sql=''
    for param in params:
        sql+= char+param +"=?,"
    return sql.rstrip(',')
def deleteImg(folder_path,file_name):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == file_name:
                file_path = os.path.join(root, file)
                os.remove(file_path)
def printRs(type,mess,data):
    rs={}
    rs['status']=type
    if mess is not None:
        rs['mess']=mess
    if data is not None:
        if len(data)==1:
            rs['data']=data[0]
        else:
            rs['data']=data
    return rs
def getURLImg(columnName,fileName):
    if columnName=='avatar':
        return f"getUrlImg/imgAvatar/{fileName}"
    elif columnName=='hinhAnh':
        return f"getUrlImg/imgXe/{fileName}"
def rsData(rows,columnName):
    columnNameImg=['avatar','hinhAnh']
    results = []
    for row in rows:
        record = {}
        for i in range(len(columnName)):
            if isinstance(row[i],datetime):
                row[i]= formatDate(row[i])
            if columnName[i] in columnNameImg:
                row[i] = getURLImg(columnName[i],row[i])
            record[columnName[i]] = row[i]
        results.append(record)
    return results

def utf8_to_slug(string):
    # Convert to ASCII characters
    string = unidecode(string)  
    # Remove special characters
    string = re.sub(r"[^\w\s-]", "", string.lower()) 
    # Replace spaces with hyphens
    string = re.sub(r"\s+", "-", string)
    string=re.sub(r"_","-",string)
    return string

def createNameImgXe(name,bienSoXe):
    name=utf8_to_slug(name)
    bienSoXe=utf8_to_slug(bienSoXe)
    return name +"-"+ bienSoXe

# listParamsAccept=['maTaiKhoan','email','hoTen','ngaySinh','cccd','sdt','diaChi','gioiTinh','avatar']


# print(listParamsAccept[1:-1])