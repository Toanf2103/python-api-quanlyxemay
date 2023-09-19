import requests
from bs4 import BeautifulSoup

# URL của bài hát bạn muốn tải
url = 'https://mp3.zing.vn/bai-hat/ZW7FDBA8.html'

# Gửi yêu cầu HTTP đến URL
response = requests.get(url)

# Kiểm tra nếu yêu cầu thành công
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích nội dung trang web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm thẻ audio
    audio_tag =  soup.find(attrs={'data-xml': True})
    
    # Kiểm tra nếu tìm thấy thẻ audio
    audio_tag = audio_tag['data-xml'].split('&key=')[-1]
    print(audio_tag)

