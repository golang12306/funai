# 微信消息网关

本文配合公众号文章《AI Agent 接进微信，就是我现在的样子》。

## 核心文件

- `gateway.py` — 消息网关 + 会话管理完整实现

## 架构

```
用户发微信 → 微信服务器 → MessageGateway → Agent.act() → 回复 → 微信服务器 → 用户
```

三个关键组件：

1. **MessageGateway**：把平台消息转成 Agent 输入，调用 Agent，把结果送回
2. **SessionManager**：每个用户独立 Agent 实例，对话历史互不干扰
3. **normalize_message**：统一不同平台（微信/飞书/QQ）的消息格式

## 运行

```python
from gateway import SessionManager, Tool, search_web, calc, send_email

tools = [
    Tool("search_web", "搜索网络", search_web),
    Tool("calc", "数学计算", calc),
    Tool("send_email", "发送邮件", send_email),
]

manager = SessionManager(tools)

# 收到微信消息后调用：
manager.handle({"from": "user_openid", "content": "帮我搜一下今天AI新闻"})
```

## 接入真实微信

将 `wechat_send_message` 和 `wechat_receive_message` 替换为真实微信 API：
- 消息接收：微信公众平台的模板消息推送或客服消息接口
- 消息发送：微信客服消息 API 或模板消息

飞书、QQ 等其他平台同理，只需在 `normalize_message` 里处理各自的格式。
