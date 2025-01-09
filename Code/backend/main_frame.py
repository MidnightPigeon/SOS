#frame of SOS backend
###
#FastAPI注意事项：
#1. 该框架需求Uvicorn启动，请先通过cmd安装fastapi与Uvicorn
#具体指令：pip install uvicorn, pip install fastapi
#后续可通过单独的文档进行安装
#2. 请在cmd中输入指令：uvicorn main_frame:app --reload以启动服务
#运行后，FastAPI 应用会在 http://127.0.0.1:8000 启动，你可以在浏览器中访问这个 URL 来看到返回的 JSON 响应。

#FastAPI 会自动为你的 API 生成文档，并且你可以通过两个 URL 查看：
#Swagger UI: http://127.0.0.1:8000/docs
#ReDoc: http://127.0.0.1:8000/redoc
#这两个接口提供了自动生成的交互式 API 文档，可以让你方便地查看 API 文档并进行测试。

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