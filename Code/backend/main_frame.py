#frame of SOS backend
"""
FastAPI注意事项：
1. 该框架需求Uvicorn启动，请先通过cmd安装fastapi与Uvicorn
具体指令：pip install uvicorn, pip install fastapi
后续可通过单独的文档进行安装

2. 请在项目终端中输入指令：uvicorn main_frame:app --reload以启动服务
需要首先重定向至Code/backend文件夹，重定向指令为：cd Code/backend
运行后，FastAPI 应用会在 http://127.0.0.1:8000 启动，你可以在浏览器中访问这个 URL 来看到返回的 JSON 响应。
终端窗口可以看到具体的访问信息，通过Ctrl+C可以关闭服务。

FastAPI 会自动为你的 API 生成文档，并且你可以通过两个 URL 查看：
Swagger UI: http://127.0.0.1:8000/docs
我们将通过这个UI对于后端进行相应的操作和测试，因此运行后直接在浏览器中输入该网址即可。
ReDoc: http://127.0.0.1:8000/redoc
这两个接口提供了自动生成的交互式 API 文档，可以让你方便地查看 API 文档并进行测试。

FastAPI官方站点：https://fastapi.tiangolo.com/
"""

"""
后端功能框架设定：
1. 通过前端接收完整剧本并保存至本地，路径为script文件夹下(已完成此项功能)。
2. 调用分词代码read_act.py，对剧本进行分词处理，并将分词结果保存至result.txt。
3. 读取result.txt并根据内容自编辑blender脚本，上传至上级目录的Animation文件夹下(已完成文本读取)。
4. 调用blender程序并注入对应的脚本，生成动画并渲染为视频，保存至Animation文件夹下。
5. 将生成的动画文件路径返回给前端，通过前端展示给用户。
"""


#导入所需库
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# 定义一个上传文件的目录（默认在script文件夹内）
UPLOAD_DIR = "./script"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 定义一个Pydantic模型用于文本输入
class TextRequest(BaseModel):
    content: str

# 定义一个Pydantic模型用于文件路径的输入
class FilePathRequest(BaseModel):
    file_path: str

# 定义读取文件的函数
def read_file(file_path: str) -> str:
    try:
        # 确保路径是安全的，防止目录遍历攻击
        base_path = './script'
        full_path = os.path.join(base_path, file_path)
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File at {full_path} not found.")
        
        # 打开文件并读取内容
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 创建一个GET路由来展示欢迎信息
@app.get("/")
def read_root():
    return {"message": "欢迎进入API测试程序，请访问 https://128.0.0.1:8000/docs 以查看API文档！"}

# 创建一个POST路由来接收文本并保存为txt文件
@app.post("/upload-text/")
async def upload_text(text: TextRequest):
    """
    输入长文本，将其保存为本地txt文件，用于接收剧本。
    格式为json，在请求体中包含一个json对象，如：{"content": "This is a long text."}
    """
    # 保存完整剧本，文件名为script_full.txt
    file_name = os.path.join(UPLOAD_DIR, "script_full.txt")

    # 将文本内容保存为文件
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text.content)

    return JSONResponse(content={"message": "Text saved successfully", "file": file_name}, status_code=200)

# 创建一个GET路由来展示文件内容
@app.get("/read-file/")
async def read_file_from_query(file_path: str = Query(..., description="The relative file path to read")):
    """
    通过参数输入文件路径以查看内容。
    用户可以输入文件路径来查看该文件的内容。
    """
    file_content = read_file(file_path)
    return {"file_content": file_content}

# 创建一个POST路由来接收JSON请求，并根据文件路径读取内容
@app.post("/read-file-json/")
async def read_file_from_json(request: FilePathRequest):
    """
    通过请求体输入文件路径以查看内容。
    请求体应该包含一个JSON对象，如：{"file_path": "result.txt"}。
    """
    file_content = read_file(request.file_path)
    return {"file_content": file_content}