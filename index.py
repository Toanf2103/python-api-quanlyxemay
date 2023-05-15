from fastapi import FastAPI
import json
import pyodbc
import uvicorn
import get
# uvicorn index:app --reload


app = FastAPI()

@app.post("/login")
def login(username:str,password:str):
    return get.checkLogin(username,password)

@app.get("/getAll")
def getall():
    return get.getAllXe()

@app.post("/addXe")
def addXe(tenXe:str,hangXe:str,trangThai:str,bienSoXe:str,loaiXe:str,giaThue:float):
    return get.addXe(tenXe,hangXe,trangThai,bienSoXe,loaiXe,giaThue)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

