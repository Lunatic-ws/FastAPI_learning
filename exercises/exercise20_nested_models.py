# 练习20：嵌套模型
#
# 目标：创建和使用嵌套 Pydantic 模型
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()
# 任务：
# 1. 创建 Image 模型（url: HttpUrl, name: str）
# 2. 创建 Item 模型（name, price, tags: set[str], images: list[Image]）
# 3. 创建 Offer 模型（name, items: list[Item]）
# 4. 创建 POST /offers/ 端点，接收 Offer
# 5. 测试发送嵌套 JSON 数据
#
# 提示：
# - url: HttpUrl 自动验证 URL 格式
# - tags: set[str] 自动去重
# - images: list[Image] 嵌套模型列表
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    price: float
    tags: set[str]
    images: list[Image]
    
class Offer(BaseModel):
    name: str
    items: list[Item]

@app.post("/offers/")
def post_offer(offer: Offer):
    return {"offer": offer}

if __name__ == "__main__":
    pass
