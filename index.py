from fastapi import FastAPI, Request,Body,Form, UploadFile
from fastapi.responses import FileResponse
from typing import List
from api import get,user,xe,order
import json
import pyodbc
import uvicorn
import os



from fastapi.middleware.cors import CORSMiddleware
# uvicorn index:app --reload


app = FastAPI()
#Lấy đường dẫn hiện tại
current_file_path = os.path.abspath(__file__)

#lấy đường dẫn Project
current_directory = os.path.dirname(current_file_path)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(rq = Body()):
    return user.checkLogin(rq)

@app.post('/addAccount')
def addAccount(rq=Body()):
    return user.addAccount(rq)

@app.post('/changePass')
def addAccount(rq=Body()):
    return user.changePass(rq)
@app.post('/updateInfoUser')
async def updateInfo(request: Request):
    form_data = await request.form()
    relative_path = os.path.join(current_directory, 'img\imgAvatar')
    return await user.updateInfoUser(form_data,relative_path)


@app.get("/getAllXe")
def getall():
    return xe.getAllXe()

@app.post("/addXe")
def addXe(tenXe:str,hangXe:str,trangThai:str,bienSoXe:str,loaiXe:str,giaThue:float):
    return xe.addXe(tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue)

@app.get("/getDonHang")
def getDonHang():
    return get.getDonHang()

@app.post("/addDonHang")
def addDonHang(maKH:str,ngayBD:str,ngayKT:str,listCar:str):
    return get.addDonHang(maKH,ngayBD,ngayKT,listCar)







@app.get("/getUrlImg/{folder}/{filename}")
async def getUrlImg(folder:str,filename:str):
    url = os.path.join(current_directory, 'img',folder,filename)
    return FileResponse(url)
if __name__ == "__main__":    
    uvicorn.run(app, host="localhost", port=5000)


#lấy đường dẫn Project




