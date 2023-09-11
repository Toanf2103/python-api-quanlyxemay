import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os

class FirebaseConnector:
    def __init__(self):
        # Khởi tạo kết nối Firebase
        service_account_path = os.path.join(os.path.dirname(__file__), 'firebase-adminsdk-lga08-1e24bbbd72.json')
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': "gs://cho-thue-xe-may.appspot.com"
        })
        self.bucket = storage.bucket()

    def upload_image(self, image_data, name_img):
        # Tải ảnh lên Firebase Storage
        blob = self.bucket.blob(f"imgXe/{name_img}")
        
        blob.upload_from_file(image_data)

        # Lấy URL tới ảnh đã tải lên
        image_url = blob.public_url

        return image_url
    def check_connection(self):
        try:
            # Kiểm tra kết nối với Firebase Storage
            blob = self.bucket.list_blobs(max_results=1)
            
            return True
        except Exception as e:
            print(f"Kết nối không thành công: {str(e)}")
            return False
        

