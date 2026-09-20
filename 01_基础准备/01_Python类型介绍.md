# Python类型介绍（Python Types Intro）

## 学习目标
- 理解Python类型提示（Type Hints）的基本概念
- 掌握常用类型注解语法
- 了解类型提示在FastAPI中的作用

## 为什么需要类型提示

Python 3.6+ 引入了类型提示（Type Hints），这是一种为变量、函数参数和返回值添加类型信息的方式。

类型提示的好处：
1. **代码可读性**：让其他开发者更容易理解代码意图
2. **IDE支持**：编辑器可以提供更好的自动补全和错误检查
3. **FastAPI集成**：FastAPI利用类型提示进行数据验证、序列化和文档生成

## 基本类型

### 简单类型

```python
# 基本类型注解
age: int = 25
name: str = "Alice"
height: float = 1.75
is_active: bool = True
```

### 函数类型注解

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def is_adult(age: int) -> bool:
    return age >= 18
```

## 容器类型

### 列表、字典、元组

```python
from typing import List, Dict, Tuple, Set

# Python 3.9+ 可以直接使用内置类型
names: list[str] = ["Alice", "Bob", "Charlie"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
coordinates: tuple[float, float] = (10.5, 20.3)
unique_ids: set[int] = {1, 2, 3, 4, 5}

# Python 3.8及以下需要从typing导入
names_old: List[str] = ["Alice", "Bob"]
scores_old: Dict[str, int] = {"Alice": 95}
```

## Optional和Union

### Optional类型

```python
from typing import Optional

# Optional[str] 等价于 str | None (Python 3.10+)
def find_user(user_id: int) -> Optional[str]:
    # 可能返回字符串，也可能返回None
    if user_id > 0:
        return f"User_{user_id}"
    return None

# Python 3.10+ 简写
def find_user_new(user_id: int) -> str | None:
    if user_id > 0:
        return f"User_{user_id}"
    return None
```

### Union类型

```python
from typing import Union

# 可以是多种类型之一
def process(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ 简写
def process_new(value: int | str) -> str:
    return str(value)
```

## 自定义类型

### 类作为类型

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

def create_user(name: str, age: int) -> User:
    return User(name, age)

def get_user_name(user: User) -> str:
    return user.name
```

### Pydantic模型（FastAPI常用）

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# FastAPI会自动验证数据类型
def create_user_endpoint(user: User):
    return {"message": f"Created user {user.name}"}
```

## 练习题

### 练习1：基础类型注解
**文件位置**: `exercises/exercise1_basic_types.py`

完成以下代码，为所有变量和函数添加类型注解：

```python
# TODO: 为以下变量添加类型注解
name = "Alice"
age = 30
height = 1.65
is_student = True

# TODO: 为以下函数添加参数和返回值类型注解
def calculate_rectangle_area(length, width):
    return length * width

def format_user_info(username, age):
    return f"User: {username}, Age: {age}"

def check_eligibility(score):
    if score >= 60:
        return True
    return False
```

### 练习2：容器类型
**文件位置**: `exercises/exercise2_container_types.py`

```python
from typing import List, Dict, Optional

# TODO: 为以下变量添加正确的容器类型注解
student_names = ["Alice", "Bob", "Charlie"]
student_scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

# TODO: 为函数添加类型注解
def get_top_students(names, scores):
    """返回分数大于90的学生列表"""
    return [name for name, score in scores.items() if score > 90]

def find_student_score(name, score_dict):
    """查找学生分数，如果不存在返回None"""
    return score_dict.get(name)
```

### 练习3：Pydantic模型
**文件位置**: `exercises/exercise3_pydantic_model.py`

```python
from pydantic import BaseModel
from typing import Optional

# TODO: 创建一个Product模型，包含以下字段：
# - name: str
# - price: float
# - quantity: int
# - description: Optional[str] (可选)

# 在这里定义Product类


# TODO: 创建一个Order模型，包含以下字段：
# - order_id: str
# - products: list[Product]
# - total_amount: float

# 在这里定义Order类


def test_models():
    # 测试代码
    product_data = {
        "name": "Laptop",
        "price": 999.99,
        "quantity": 5,
        "description": "Gaming Laptop"
    }
    
    # TODO: 使用Product模型验证数据
    # product = Product(**product_data)
    # print(product)
    
    pass

if __name__ == "__main__":
    test_models()
```

## 完成练习后

完成上述练习后，运行以下命令进行测试：
```bash
python exercises/exercise1_basic_types.py
python exercises/exercise2_container_types.py
python exercises/exercise3_pydantic_model.py
```

准备好后，请告知我检查批改你的练习！

## 参考资源
- [Python Type Hints官方文档](https://docs.python.org/3/library/typing.html)
- [FastAPI Python Types文档](https://fastapi.tiangolo.com/python-types/)
