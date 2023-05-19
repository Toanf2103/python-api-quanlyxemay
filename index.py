from fastapi import FastAPI, Request,Body,Form, UploadFile
from typing import List
from api import get
import json
import pyodbc
import uvicorn


from fastapi.middleware.cors import CORSMiddleware
# uvicorn index:app --reload


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(rq = Body()):
    return get.checkLogin(rq)

@app.get("/getAll")
def getall():
    return get.getAllXe()

@app.post("/addXe")
def addXe(tenXe:str,hangXe:str,trangThai:str,bienSoXe:str,loaiXe:str,giaThue:float):
    return get.addXe(tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue)

@app.get("/getDonHang")
def getDonHang():
    return get.getDonHang()

@app.post("/addDonHang")
def addDonHang(maKH:str,ngayBD:str,ngayKT:str,listCar:str):
    return get.addDonHang(maKH,ngayBD,ngayKT,listCar)

@app.post("/test")
async def test(request: Request):
    data=await request.json()
    print("asdasjdhgfasghjdfjaghsdhjagsf", data)
    print(data.get("username"),data.get("password"))
    return get.test(data.get("username"),data.get("password"))

@app.post("/testImg")
async def upload_images(images: List[UploadFile] = Form(), name: str = Form(...), password: str = Form(...)):
    
    
    return await get.testImg(images, name, password)

@app.post("/process_form")
async def create_item(request: Request):
    form_data = await request.form()
    item_name = form_data["name"]
    item_description = form_data["password"]
    # Xử lý dữ liệu form
    # ...
    return {"message": form_data["name"]}
if __name__ == "__main__":    
    uvicorn.run(app, host="localhost", port=5000)
