import pyodbc
class connect():
    def __init__(self):
            # Thông tin cơ sở dữ liệu
        server = 'SQL8001.site4now.net'
        database = 'db_a9917c_quanlyxemay'
        username = 'db_a9917c_quanlyxemay_admin'
        password = 'quanlyxemay1'

        # Tạo chuỗi kết nối
        connection_string = 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()
    
    
