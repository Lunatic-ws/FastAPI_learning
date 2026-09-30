# 31 高级Python类型

## 学习目标

- 理解 `Optional` 与 `Union` 的真实含义
- 掌握在类型注解中选择正确的联合类型写法

## 核心概念

### 1. Union 或 Optional

当代码不能使用 `|`（例如在 `response_model=` 这类**参数值**里，而不是注解位置），用 `typing.Union` 代替竖线：

```python
from typing import Union

def say_hi(name: Union[str, None]):
    print(f"Hi {name}!")
```

### 2. Optional 的命名陷阱

`Optional[SomeType]` 与 `Union[SomeType, None]` 完全等价，但 "optional（可选）" 这个词容易误导：

```python
from typing import Optional

def say_hi(name: Optional[str]):
    print(f"Hey {name}!")

say_hi()          # ❌ 报错！name 不是"可选参数"，它是必填的
say_hi(name=None) # ✅ 正确：None 是有效取值
```

- `Optional[str]` 的意思是"取值可以是 str **或 None**"，不代表"参数可以不传"
- 是否可选（能否不传）由**有没有默认值**决定，与 Optional 无关

### 3. 作者建议

FastAPI 作者的主观建议：

- 🚨 避免使用 `Optional[SomeType]`
- ✨ 改用 `Union[SomeType, None]`——含义更直白

### 4. 大多数时候直接用 `|`

Python 3.10+ 的注解里直接用竖线即可：

```python
def say_hi(name: str | None):
    print(f"Hi {name}!")
```

这也是 FastAPI 文档示例的主流写法（本知识库其他文档中的 `str | None = None` 即是）。

### 5. FastAPI 中联合类型的实际用途

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None   # 请求体字段可缺省

@app.post("/items/")
async def create_item(item: Item):
    return item
```

- 响应模型/请求模型字段：`str | None = None` 表示可缺省
- `Union[int, str]` 类型的字段：FastAPI 会按声明顺序尝试验证

## 最佳实践

1. **新代码一律用 `|` 语法**（Python 3.10+）
2. **参数值位置（非注解）才用 `typing.Union`**，如 `response_model=Union[A, B]` 这类运行时表达式的兼容场景
3. **分清"取值可为 None"与"参数可省略"**：前者是类型，后者是默认值

## 常见问题

**Q: Optional[X] 和 X | None 有区别吗？**
A: 运行时完全等价，仅写法与语义清晰度不同

**Q: 为什么我的 response_model=Union[ModelA, ModelB] 校验总走第一个？**
A: Pydantic 按 union 成员顺序逐一尝试，第一个匹配成功的胜出；类型差异太小时建议用 discriminated union（tag 判别字段）

## 相关章节

- [01_Python类型介绍_已掌握.md](../01_基础准备/01_Python类型介绍_已掌握.md) - Python 类型基础
- [10_嵌套模型.md](../02_教程-用户指南/10_嵌套模型.md) - 嵌套模型
- [12_额外数据类型.md](../02_教程-用户指南/12_额外数据类型.md) - 额外数据类型
