# 练习59：直接返回Response（Return a Response Directly）
# 本练习文件只有注释，请在下方编写代码实现
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

app = FastAPI()

"""
任务1: 直接返回JSONResponse
要求:
- 创建GET接口 /json-response/
- 直接return JSONResponse(content={"message": "Hello"}, status_code=200)
- （需要 from fastapi.responses import JSONResponse）
"""
@app.get("/json-response/")
def get_json_response() -> JSONResponse:
    return JSONResponse(content={"message": "Hello"}, status_code=200)


"""
任务2: 直接返回带自定义头的Response
要求:
- 创建GET接口 /raw-response/
- return Response(content="原始内容", media_type="text/plain", headers={"X-Custom": "abc"})
"""
@app.get("/raw-response/")
def get_raw_response() -> Response:
    return Response(
        content="原始内容",
        media_type="text/plain",
        headers={"X-Custom": "abc"},
    )


class Item(BaseModel):
    name: str
    price: float


class Item2(BaseModel):
    name: str
    price: float


items = {
    1: {"name": "Portal Gun", "price": 42.0, "secret_code": "s3cr3t"},
    2: {"name": "Hoverboard", "price": 299.0, "secret_code": "s3cr3t"},
}

"""
任务3: 直接返回与response_model的关系
要求:
- 创建接口声明了response_model=Item，但直接return一个JSONResponse
- 在注释中回答：此时response_model还会过滤数据吗
- 文档中的响应模型展示是否还正常
"""
@app.post("/items/", response_model=Item)
def create_item() -> JSONResponse:
    return JSONResponse(
        content={"name": "Bypass", "price": 1.0, "secret_code": "s3cr3t"},
        status_code=201,
        headers={"X-Response-Model": "bypassed"},
    )


@app.get("/items/dict/", response_model=Item2)
def read_item_dict() -> dict:
    return {"name": items[1]["name"], "price": items[1]["price"], "secret_code": "s3cr3t"}


"""
任务4: 直接返回dict vs Response对比
要求:
- 创建两个接口：一个return普通dict，一个return JSONResponse
- 在注释中记录两者的差异（序列化、headers控制、cookies控制）
"""
@app.get("/dict-response/")
def get_dict_response() -> dict:
    return {"message": "普通dict", "serialized_by": "FastAPI默认的JSONResponse"}


@app.get("/dict-vs-json/")
def get_dict_vs_json() -> JSONResponse:
    return JSONResponse(
        content={"message": "JSONResponse", "serialized_by": "我自己创建并控制"},
        status_code=201,
        headers={"X-Custom": "json-response"},
    )

# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
