# import os
# img_dir = "testHTMLAPI"
# test_file = "testHTMLAPI/test.txt"
# try:
#     with open(test_file, "w") as file:
#         file.write("This is a test file.")
#     print("Bạn có quyền ghi vào thư mục img.")
# except IOError:
#     print("Bạn không có quyền ghi vào thư mục img.")
# finally:
#     if os.path.exists(test_file):
#         os.remove(test_file)

from api.Connect import connect
from api.xuli import *
import pyodbc



conn = connect()
cursor = conn.cursor
connection= conn.connection
# try:
#     taiKhoan='Tioanf121qweqwe'
#     matKhau='asdasd'
#     phanQuyen='Khách hàng'
#     hoTen='asdaskldjtoan'
#     email='22@gmail.com'  
#     gioiTinh='M'
#     cursor.execute("SET DATEFORMAT dmy")
#     cursor.execute("EXEC pr_add_account @taiKhoan=?, @matKhau=?,@phanQuyen=?,@hoTen=?,@email=?,@gioiTinh=?",taiKhoan,matKhau,phanQuyen,hoTen,email,gioiTinh)
#     connection.commit()
#     conn.close()
#     print(True)
# except pyodbc.Error as ex:
#     print(ex)

taiKhoan='qwe12321'
sql=f"select * from TaiKhoan where taiKhoan='{taiKhoan}'"
cursor.execute(sql)
rows = cursor.fetchone()
if rows:
    print(1)
else:
    print(2)