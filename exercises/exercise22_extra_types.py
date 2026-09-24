# 练习22：额外数据类型
# 
# 学习目标：
# 1. 使用 UUID 类型
# 2. 使用 datetime 相关类型
# 3. 使用其他高级数据类型
# 4. 理解数据类型的自动转换

# TODO: 导入必要的模块
from datetime import datetime, date, time, timedelta
from typing import Annotated
from uuid import UUID
from decimal import Decimal
from fastapi import FastAPI, Body, Query

# TODO: 创建 FastAPI 应用实例
app = FastAPI()

# TODO: 创建一个端点，使用 UUID 作为路径参数
# 路径: /items/{item_id}
# 参数: item_id (UUID 类型)
# 返回: {"item_id": item_id, "item_id_str": str(item_id)}
@app.get("/items/{item_id}")
def get_item(item_id: UUID):
    return {"item_id": item_id, "item_id_str": str(item_id)}

# TODO: 创建一个端点，使用 datetime 参数
# 路径: /events/
# 查询参数:
#   - start_time: datetime
#   - end_time: datetime
# 返回: 包含时间信息和持续时间的字典
@app.get("/events/")
def get_events(start_time: datetime, end_time: datetime):
    duration = end_time - start_time
    return {"start_time": start_time, "end_time": end_time, "duration": duration}

# TODO: 创建一个端点，使用 date 和 time 参数
# 路径: /schedule/
# 查询参数:
#   - event_date: date
#   - event_time: time
# 返回: 包含日期和时间信息的字典
@app.get("/schedule/")
def get_schedule(event_date: date, event_time: time):
    return {"event_date": event_date, "event_time": event_time}

# TODO: 创建一个端点，使用 timedelta 参数
# 路径: /duration/
# 请求体:
#   - duration: timedelta (以秒为单位的 float)
# 返回: 包含持续时间信息的字典
@app.post("/duration/")
def post_duration(duration: Annotated[timedelta, Body()]):
    return {
        "duration": duration,
        "total_seconds": duration.total_seconds(),
        "days": duration.days,
        "seconds": duration.seconds
    }

# TODO: 创建一个端点，使用 Decimal 类型
# 路径: /price/
# 查询参数:
#   - amount: Decimal
#   - tax_rate: Decimal
# 返回: 包含价格计算结果的字典
@app.get("/price/")
def get_price(amount: Decimal, tax_rate: Decimal):
    result = amount * (1 + tax_rate)
    return {"amount": amount, "tax_rate": tax_rate, "result": result}

# TODO: 创建一个端点，使用 bytes 类型
# 路径: /data/
# 请求体:
#   - binary_data: bytes
# 返回: {"length": len(binary_data), "data": binary_data}
@app.post("/data/")
def get_data(binary_data: bytes):
    return {"length": len(binary_data), "data": binary_data} # FastAPI 自动转为 base64 字符串

# TODO: 创建一个综合端点，使用多种高级数据类型
# 路径: /complex/{resource_id}
# 路径参数:
#   - resource_id: UUID
# 查询参数:
#   - created_after: datetime (可选)
# 请求体:
#   - expiry: timedelta
#   - precision: Decimal
# 返回: 包含所有信息和计算结果的字典
@app.post("/complex/{resource_id}")
def post_complex(
    resource_id: UUID,
    expiry: Annotated[timedelta, Body()], # 到期时长
    precision: Annotated[Decimal, Body()], # 精度
    created_after: datetime | None = None # 创建时间晚于
):
    result = {
        "resource_id": resource_id,
        "created_after": created_after,
        "expiry": expiry,
        "precision": precision
    }

    if created_after:
        result["expiry_time"] = created_after + expiry
    return result

if __name__ == "__main__":
    pass
