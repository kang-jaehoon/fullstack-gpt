# LangChain expression language를 사용하고, 그 결과값으로 또라든 Chain을 실행할 수 있다..
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler

chat = ChatOllama(
    model="phi3:medium",
    temperature=0.1,
    streaming=True,
    callbacks=[
        StreamingStdOutCallbackHandler(),
    ]
)

# 월클 요리사는 레시피를 제공한다.
chef_template = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class international chef. You create easy to floow recipies for any type of cuisine with easy to find ingredients."),
    ("human", "I want to cook {cuisine} food."),
])

chef_chain = chef_template | chat

# 채식주의자 요리사는 월클 요리사의 레시피를 채식으로 변경한다.
veg_chef_template = ChatPromptTemplate.from_messages([
    ("system", "You are a vegetarian chef specialized on making traditional recipies vegetarian. You find alternative ingredients and explain their preparation. You don't radically modify the recipe. If there is no alternative for a food just say you don't know how to replace it."),
    ("human", "{recipe}"),
])

veg_chain = veg_chef_template | chat

final_chain = {"recipe": chef_chain} | veg_chain

final_chain.invoke({
    "cuisine": "indian"
})

