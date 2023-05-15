from fastapi import FastAPI
import json
import pyodbc
import uvicorn
import get
# uvicorn index:app --reload


app = FastAPI()


@app.get("/getAll")
def getall():
    return get.getAllXe()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

