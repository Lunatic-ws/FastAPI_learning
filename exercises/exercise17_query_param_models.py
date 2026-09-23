# 练习17：查询参数模型
# 
# 目标：使用 Pydantic 模型组织查询参数
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Literal, Annotated

app = FastAPI()
# 任务：
# 1. 创建一个 FilterParams 模型，包含 limit（int类型，默认100，范围1-100）、offset（int类型，默认0，>=0）、sort（Literal类型）
# 2. 创建一个 GET /items/ 端点，使用 FilterParams 作为查询参数模型
# 3. 使用 Annotated 和 Query() 声明参数
# 4. 测试访问 /items/?limit=50&offset=10&sort=created_at
#
# 提示：
# - limit: int = Field(100, gt=0, le=100)
# - offset: int = Field(0, ge=0)
# - sort: Literal["created_at", "updated_at"] = "created_at"
class FilterParams(BaseModel):
    limit: int = Field(100, ge=1, le=100)
    offset: int = Field(0, ge=0)
    sort: Literal["created_at", "updated_at"] = "created_at"

@app.get("/items/")
def get_item(filterparam: Annotated[FilterParams, Query()]):
    return {"filterparam": filterparam}

if __name__ == "__main__":
    pass
