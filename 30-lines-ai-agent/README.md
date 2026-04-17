# 30行代码 AI Agent

用最少的代码，感受 AI Agent 的核心原理。

## 核心代码

```python
class Tool:
    def __init__(self, name, desc, func):
        self.name = name
        self.desc = desc
        self.func = func

class Agent:
    def __init__(self, tools):
        self.tools = {t.name: t for t in tools}
        self.history = []

    def think(self, msg):
        resp = llm([
            {"role": "system", "content": tool_prompt(list(self.tools.values()))},
            *self.history,
            {"role": "user", "content": msg}
        ])
        self.history.append({"role": "user", "content": msg})
        self.history.append({"role": "assistant", "content": resp})
        return resp

    def parse_tool(self, text):
        import re
        m = re.search(r'<tool>(.*?)</tool>', text, re.DOTALL)
        if not m:
            return None
        name = re.search(r'<name>(.*?)</name>', m.group(1)).group(1)
        args = re.search(r'<args>(.*?)</args>', m.group(1)).group(1)
        return {"name": name, "func": self.tools[name].func, "args": eval(args)}

    def act(self, msg):
        resp = self.think(msg)
        while (call := self.parse_tool(resp)):
            result = call["func"](**call["args"])
            resp = self.think(f"[tool] {result}")
        return resp
```

## 工具示例

```python
def search_web(query):
    return f"[搜索结果] {query} 相关的内容..."

def calc(expr):
    return str(eval(expr))

def send_email(to, content):
    return f"[邮件已发] 收件人: {to}, 内容: {content}"
```

## 使用方法

```python
agent = Agent([
    Tool("search_web", "搜索网络", search_web),
    Tool("calc", "数学计算", calc),
    Tool("send_email", "发送邮件", send_email),
])

result = agent.act("北京今天多少度？如果超过30度就发邮件告诉老婆今晚不带外套")
print(result)
```

## 接入微信/飞书

见 `wechat-gateway/` 目录——消息网关、会话管理、渠道接入的完整实现。

## 完整示例

见 `agent.py`
