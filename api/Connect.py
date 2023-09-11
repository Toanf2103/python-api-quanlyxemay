import pyodbc
class connect():

    def __init__(self):
            # Thông tin cơ sở dữ liệu
        server = 'MSI'
        database = 'QuanLyXeMay'
        username = 'sa'
        password = 'kutoan1346'

        # Tạo chuỗi kết nối
        connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def dataNotExist(self,ten_bang,ten_cot,gia_tri):
        sql=f"SELECT * from {ten_bang} where {ten_cot}='{gia_tri}'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row is None:
            return True
        return False
    
    
