import os
img_dir = "testHTMLAPI"
test_file = "testHTMLAPI/test.txt"
try:
    with open(test_file, "w") as file:
        file.write("This is a test file.")
    print("Bạn có quyền ghi vào thư mục img.")
except IOError:
    print("Bạn không có quyền ghi vào thư mục img.")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)