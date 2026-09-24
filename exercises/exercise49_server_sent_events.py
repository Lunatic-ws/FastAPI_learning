# 练习49：服务器发送事件（SSE）
#
# 目标：使用SSE流式传输数据到客户端
#
# 任务：
# 1. 导入 EventSourceResponse 和 ServerSentEvent
# 2. 创建 GET /stream 端点，设置 response_class=EventSourceResponse
# 3. 使用 yield ServerSentEvent(data=item) 发送事件
# 4. 实现一个断点续传功能，读取 Last-Event-ID 头
#
# 提示：
# - 导入 from fastapi.sse import EventSourceResponse, ServerSentEvent
# - ServerSentEvent可设置 data, event, id, retry, comment 字段
# - 使用 raw_data 发送未经JSON编码的原始文本
# - 浏览器通过 EventSource API 接收SSE

if __name__ == "__main__":
    pass
