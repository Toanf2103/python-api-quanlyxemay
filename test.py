from unidecode import unidecode
import re
import pyodbc
import os
from api.Connect import connect
import datetime
from datetime import date

def formatDate(ngay):
    formatType="%d-%m-%Y"
    return ngay.strftime(formatType)


def utf8_to_slug(string):
    # Convert to ASCII characters
    string = unidecode(string)  
    # Remove special characters
    string = re.sub(r"[^\w\s-]", "", string.lower()) 
    # Replace spaces with hyphens
    string = re.sub(r"\s+", "-", string)
    string=re.sub(r"_","-",string)
    string=re.sub(r";","",string)
    return string

# sql="select * from TaiKhoan"
# conn = connect()
# cursor = conn.cursor
# cursor.execute(sql)
# rows = cursor.fetchall()

# print(list(record))
# for x in list(record):
#     print(dict(x))


# columns = [column[0] for column in cursor.description]
# print(columns)


# results = []
# for row in rows:
#     record = {}
#     for i in range(len(columns)):
#         if isinstance(row[i],datetime.datetime):
#             row[i]= formatDate(row[i])
#         record[columns[i]] = row[i]
        
#     results.append(record)
# # In kết quả
# for result in results:
#     print(result)

# listParamsInfo=['maTaiKhoan','email','hoTen','ngaySinh','cccd','sdt','diaChi','gioiTinh','avatar']
# string=''
# for x in listParamsInfo[1:]:
#     string+= x +"=%s,"

# print(string)

# folder_path="d:\Hoc\Đồ án phần mềm\API_XE\img\imgAvatar"
# file_name = "KH00000002.jpeg"
# for root, dirs, files in os.walk(folder_path):
#     for file in files:
#         if file == file_name:
#             file_path = os.path.join(root, file)
#             os.remove(file_path)
#             print(f"Đã xóa tệp tin: {file_path}")

print(4/3)
