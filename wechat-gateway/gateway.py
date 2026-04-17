"""
微信消息网关 - 将 AI Agent 接入微信消息流
"""
import json
from agent import Agent, Tool

# ========== 模拟的微信 API（实际使用时替换为真实微信 API）==========

def wechat_receive_message():
    """模拟：从微信服务器拉取一条消息，实际项目中这里换成你的 webhook 接收逻辑"""
    # 真实场景：webhook POST /wechat -> 返回 {"from": "user_openid", "content": "..."}
    raise NotImplementedError("请替换为真实微信消息接收逻辑")

def wechat_send_message(to_user, content):
    """模拟：发送回复给用户，实际项目中替换为真实微信 API"""
    # 真实场景：POST 到微信模板消息或客服消息接口
    print(f"[微信发送] To: {to_user}, Content: {content}")

# ========== 消息网关==========

class MessageGateway:
    def __init__(self, agent):
        self.agent = agent

    def handle_incoming(self, message):
        """
        处理一条 incoming 消息
        message 格式: {"from": "user_openid", "content": "用户输入文字"}
        """
        user_id = message.get("from", "unknown")
        user_input = message.get("content", "")
        if not user_input:
            return

        # 调用 Agent 处理，Agent 只管业务逻辑，不管消息从哪来
        reply = self.agent.act(user_input)

        # 把回复通过微信发回去
        wechat_send_message(user_id, reply)

    def normalize_message(self, raw):
        """
        不同平台消息格式不同，在这里统一转换
        微信消息是 XML，飞书是 JSON，QQ 是另一种 JSON
        """
        # 实际按平台分别处理
        return {
            "from": raw.get("from") or raw.get("sender_open_id", ""),
            "content": raw.get("content") or raw.get("text", ""),
        }


# ========== 会话管理：每个用户有独立的 Agent 实例==========

class SessionManager:
    def __init__(self, tools):
        self.sessions = {}  # user_id -> Agent
        self.tools = tools

    def get_agent(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = Agent(self.tools)
        return self.sessions[user_id]

    def handle(self, message):
        normalized = message  # 假设已经 normalize 过了
        user_id = normalized.get("from", "unknown")
        agent = self.get_agent(user_id)
        gateway = MessageGateway(agent)
        gateway.handle_incoming(normalized)


# ========== 工具函数==========

def search_web(query):
    """搜索网络（示例）"""
    return f"[搜索结果] 关于「{query}」的内容：..."


def calc(expr):
    """数学计算"""
    return str(eval(expr))


def send_email(to, content):
    """发送邮件（示例）"""
    return f"[邮件已发] 收件人: {to}, 内容: {content}"


# ========== 启动==========

if __name__ == "__main__":
    tools = [
        Tool("search_web", "搜索网络", search_web),
        Tool("calc", "数学计算", calc),
        Tool("send_email", "发送邮件", send_email),
    ]

    manager = SessionManager(tools)

    # 模拟收到一条微信消息
    test_message = {
        "from": "user_001",
        "content": "帮我搜一下今天有什么AI新闻"
    }
    manager.handle(test_message)
