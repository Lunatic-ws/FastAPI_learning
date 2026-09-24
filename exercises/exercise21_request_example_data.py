# 练习21：声明请求示例数据
# 要求：根据注释要求实现相应的FastAPI应用
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# 题目1：Body的example参数
# 创建一个PUT接口 /items/{item_id}
# Item模型: name(str), description(可选str), price(float), tax(可选float)
# 使用 Body 的 example 参数声明一个完整的请求示例
# 在 /docs 中查看请求体示例是否显示
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
def put_items(
    item_id: int,
    item: Annotated[
        Item, 
        Body(
            example={
                "name": "foo",
                "description": "A very nice Item",
                "price": 26.5,
                "tax":4.5
            }
        )
    ]
):
    return {"item_id": item_id, "item": item}

# 题目2：Body的examples参数
# 创建一个PUT接口 /items2/{item_id}
# 使用 Body 的 examples 参数传入字典
# 键为示例名，值为包含 summary 和 value 的字典
# 至少提供2个示例（如：完整示例、仅必填字段的最小示例）
@app.put("/items2/{item_id}")
def put_items2(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples={
                "完整示例":{
                    "summary": "这是一个完整示例",
                    "value":{
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    }
                },
                "最小示例":{
                    "summary": "这是最小示例",
                    "value":{
                        "name": "test",
                        "price": 32.5
                    }
                }
            }
        )
    ]
):
    return {"item_id": item_id, "item": item}

# 题目3：Pydantic的Field example
# 在Item模型的description字段上使用 Field(example="一台黑色的电视机")
# 在 /docs 中查看字段级示例的显示效果
class Item1(BaseModel):
    name: str
    description: str | None = Field(default=None, example="一台黑色的电视机")
    price: float
    tax: float | None = None

# 题目4：模型级json_schema_extra
# 创建Item模型，通过 model_config = {"json_schema_extra": {"examples": [...]}}
# 声明模型级别的请求示例
# 对比题目2的Body示例与模型示例在文档中的展示差异
class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]
        }
    }
    
# 题目5：嵌套模型的示例
# 创建Tag模型: name(str)
# 创建Item模型包含 tags: list[Tag]
# 为Tag模型单独声明示例，观察嵌套模型示例在文档中的效果
class Tag(BaseModel):
    name: str = Field(examples=["电子", "家具", "食品"])
class Item3(BaseModel):
    tags: list[Tag]


# 在下方编写你的代码实现
if __name__ == "__main__":
    import uvicorn
    # 在这里启动FastAPI应用
    # uvicorn.run(app, host="0.0.0.0", port=8000)
