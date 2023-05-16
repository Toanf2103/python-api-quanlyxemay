from fastapi import FastAPI, Request,Body
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
def login(username:str,password:str):
    return get.checkLogin(username,password)

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
def test(request: Request):
    rq = request.json() 
    print(rq['listCar']) 
    return get.test(rq['listCar'])

if __name__ == "__main__":
    
    uvicorn.run(app, host="localhost", port=5000)
