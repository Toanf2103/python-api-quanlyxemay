import pyodbc

def check_vong_dau():
    # Thông tin cơ sở dữ liệu
    server = 'SQL8001.site4now.net'
    database = 'db_a9917c_testsql'
    username = 'db_a9917c_testsql_admin' 
    password = 'kutoan1346'

    # Tạo chuỗi kết nối
    connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

    # Kết nối tới cơ sở dữ liệu
    connection = pyodbc.connect(connection_string)

    # Thực hiện các truy vấn
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM HangXe')
    rows = cursor.fetchall()
    

    data_array = []
    for row in rows:
        data_array.append(row)

    cursor.close()
    connection.close()
    return data_array

for item in check_vong_dau():
    print(type(item))