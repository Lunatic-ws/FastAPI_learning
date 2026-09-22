# 练习1：基础类型注解
# 要求：为以下变量和函数添加类型注解

# 题目1：为以下变量添加类型注解
name: str = "Alice"
age: int = 30
height: float = 1.65
is_student: bool = True


# 题目2：为以下函数添加参数和返回值类型注解
def calculate_rectangle_area(length: float, width: float) -> float:
    return length * width

def format_user_info(username: str, age: int) -> str:
    return f"User: {username}, Age: {age}"

def check_eligibility(score: int) -> bool:
    if score >= 60:
        return True
    return False
