import os
from langchain_community.chat_models import ChatZhipuAI
from langchain.messages import AIMessage, HumanMessage, SystemMessage

os.environ["ZHIPUAI_API_KEY"] = "e8838101845c473bb9626b3707ffc69f.vX4ocLyxLmwMMnV5"
api_key = "e8838101845c473bb9626b3707ffc69f.vX4ocLyxLmwMMnV5"
baseUrl="https://open.bigmodel.cn/api/paas/v4/"

messages = [
    AIMessage(content="你好."),
    SystemMessage(content="你是一个大型语言模型."),
    HumanMessage(content="你是4.7版本吗"),
]

chat = ChatZhipuAI(
    model="glm-4.7",
    temperature=0.6
)

response = chat.invoke(messages)
print(response.content)