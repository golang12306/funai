# 30行代码 AI Agent

用 Python 和 x86 汇编分别实现同一个最小 AI Agent。

## 核心代码

```python
class Agent:
    def __init__(self, tools):
        self.tools = tools
        self.history = []

    def think(self, msg):
        resp = llm([
            {"role": "system", "content": tool_prompt(self.tools)},
            *self.history,
            {"role": "user", "content": msg}
        ])
        self.history.append({"role": "user", "content": msg})
        self.history.append({"role": "assistant", "content": resp})
        return resp

    def act(self, msg):
        resp = self.think(msg)
        while (call := parse_tool(resp)):
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

## 完整示例

见 `agent.py`