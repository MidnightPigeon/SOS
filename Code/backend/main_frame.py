#frame of SOS backend
###
#FastAPI注意事项：
#1. 该框架需求Uvicorn启动，请先通过cmd安装fastapi与Uvicorn
#具体指令：pip install uvicorn, pip install fastapi
#2. 请在cmd中输入指令：uvicorn main_frame:app --reload以启动服务
#目前本程序为测试程序，仅返回Hello, World!

#FastAPI官方站点：https://fastapi.tiangolo.com/
###

#导入所需库
import sys
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}