from api.Connect import connect
from api.xuli import *
import pyodbc
import os


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

def test(username,password):
    # print(type(listCar))
    
    return {
        'username':username,
        'password':password
    }



async def testImg(images, name, password):
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    ongnoi=os.path.dirname(current_directory)
    
    relative_path = os.path.join(ongnoi, 'testHtml\imgXe')
    print('ong noui',ongnoi)
    print(relative_path)
    for x in images:
        print(x.filename)
        save_path = f"{relative_path}\{x.filename}"
        with open(save_path, "wb") as file:
            file.write(await x.read())
    print({
        'username':name,
        'password':password
    })
    return {
        'username':name,
        'password':password
    }

