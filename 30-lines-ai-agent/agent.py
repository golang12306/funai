"""
30行代码 AI Agent - Python 实现
"""
import openai


def llm(messages):
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return resp.choices[0].message.content


def tool_prompt(tools):
    desc = "\n".join([f"- {t['name']}: {t['desc']}" for t in tools])
    return f"你是一个AI助手，有以下工具可用：\n{desc}\n当需要信息时使用工具，返回结果后继续推理，直到任务完成。"


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


# ========== 示例工具 ==========

def search_web(query):
    return f"[搜索结果] {query} 相关的内容..."


def calc(expr):
    return str(eval(expr))


def send_email(to, content):
    return f"[邮件已发] 收件人: {to}, 内容: {content}"


# ========== 使用 ==========
if __name__ == "__main__":
    agent = Agent([
        Tool("search_web", "搜索网络", search_web),
        Tool("calc", "数学计算", calc),
        Tool("send_email", "发送邮件", send_email),
    ])

    result = agent.act("北京今天多少度？如果超过30度就发邮件告诉老婆今晚不带外套")
    print(result)