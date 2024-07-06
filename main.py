## LLM, ChatModel 두가지를 호출해보자.
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOllama

llm = OpenAI(model="http://localhost:3300/v1")

a = llm.predict("How many planets are there?")

print(a)
