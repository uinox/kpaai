from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """你是一位擅长用双关语表达的专家天气预报员。

你可以使用两个工具：
- get_weather_for_location: 用于获取特定地点的天气
- get_user_location: 用户获取用户的位置

如果用户询问天气，请确保你知道具体位置。如果从问题中可以判断他们指的是自己所在的位置，请使用 get_user_location 工具来查找他们的位置。
"""
@dataclass
class Context:
    """自定义运行时上下文模式。"""
    user_id: str

@tool
def get_weather_for_location(city: str) -> str:
    """获取指定城市的天气。"""
    return f"{city}总是阳光明媚！"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """根据用户 ID 获取用户的位置。"""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

model = init_chat_model(
    "anthropic:claude-sonnet-4-5", 
    temperature=0
)

@dataclass
class ResponseFormat:
    """代理的响应格式。"""
    punny_response: str
    weather_conditions: str | None = None

checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "今天天气怎么样？"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])