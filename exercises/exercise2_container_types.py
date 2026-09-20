# 练习2：容器类型

# 题目1：为以下变量添加正确的容器类型注解
student_names: list[str] = ["Alice", "Bob", "Charlie"]
student_scores: dict[str, int] = {"Alice": 95, "Bob": 87, "Charlie": 92}

# 题目2：为函数添加类型注解
def get_top_students(names: list[str], scores: dict[str, int]) -> list[str]:
    """返回分数大于90的学生列表"""
    return [name for name, score in scores.items() if score > 90]

def find_student_score(name: str, score_dict: dict[str, int]) -> int | None:
    """查找学生分数，如果不存在返回None"""
    return score_dict.get(name)