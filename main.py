from langchain.chat_models import ChatOllama

chat = ChatOllama(
    model="llama3"
)

b = chat.predict("행성은 몇 개 있나요?")

print(b)