import time
from typing import Dict, List
from uuid import UUID
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
import streamlit as st
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.llms.ollama import Ollama
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.callbacks.base import BaseCallbackHandler


class ChatCallbackHandler(BaseCallbackHandler):
  
  message = ""
  
  
  def on_llm_start(self, *args, **kwargs):
    # with st.sidebar:
    #   st.write("llm started!")
    self.message_box = st.empty()  
      
  def on_llm_end(self, *args, **kwargs):
    save_message(self.message, "ai")
    # with st.sidebar:
    #   st.write("llm ended!")
  
  def on_llm_new_token(self, token: str, *args, **kwargs):
    print(token) 
    self.message += token
    self.message_box.markdown(self.message)
      

llm = Ollama(
  model="llama3:latest",
  temperature=0.1,
  callbacks=[
    ChatCallbackHandler(),
  ]
)

def save_message(message, role):
  st.session_state["messages"].append({"message": message, "role": role})
  

def send_message(message, role, save=True):
  with st.chat_message(role):
      st.markdown(message)
  if save:
      # st.session_state["messages"].append({"message": message, "role": role})
      save_message(message, role)

def paint_history():
  for message in st.session_state["messages"]:
    send_message(message["message"], message["role"], save=False,)

def format_docs(docs):
  return "\n\n".join(document.page_content for document in docs)

prompt = ChatPromptTemplate.from_messages([
  ("system", 
   """
   Answer the question using ONLY the floowing context. If you don't know the answer just say you don't know. DON'T make anything up.
   
   Context: {context}
   """,
   ),
  ("human", "{question}")
])

# 페이지 설정을 지정합니다. 페이지 제목과 아이콘을 설정합니다.
st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)

# if "messages" not in st.session_state:
#   st.session_state["messages"] = []

@st.cache_data(show_spinner="Embedding file...")
def embed_file(file):
  # st.write(file)
  file_content = file.read()
  file_path = f"./.cache/files/{file.name}"
  # st.write(file_content, file_path)
  with open(file_path, "wb") as f:
    f.write(file_content)
  cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
  splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=200,
    chunk_overlap=50
  )
  loader = UnstructuredFileLoader(file_path)
  docs = loader.load_and_split(text_splitter=splitter)
  embeddings = OllamaEmbeddings(
    base_url="http://localhost:11434",  # 모델 서버의 URL
    model="llama3:latest"
  )
  cache_embeddings = CacheBackedEmbeddings.from_bytes_store(
    embeddings, cache_dir
  )
  vectorstore = FAISS.from_documents(docs, cache_embeddings)
  retriever = vectorstore.as_retriever()
  # docs = retriver.invoke("ministry of truth")
  # st.write(docs)
  return retriever
  
  

# 페이지의 제목을 설정합니다.
st.title("DocumentGPT")

st.markdown("""
Welcome!

Use this chatbot to ask questions to an AI about your files!

Upload your files on the sidebar.
""")

with st.sidebar:
  file = st.file_uploader(
    "Upload a .txt .pdf or .docx file",
    type=["pdf", "txt", "docx"],
  )


if file:
  retriever = embed_file(file)
  send_message("I'm ready! Ask away!", "ai", save=False)
  paint_history()
  message = st.chat_input("Ask anything about your file...")
  # st.write("🔥".join(["a", "b", "c"]))
  if message:
      send_message(message, "human")
      chain = (
          {
              "context": retriever | RunnableLambda(format_docs),
              "question": RunnablePassthrough(),
          }
          | prompt
          | llm
      )
      with st.chat_message("ai"):
        chain.invoke(message)
      # send_message(response, "ai")
    # chain.invoke(message)
    # docs = retriver.invoke(message)
    # st.write(docs)
    # prompt = template.format_messages(context=docs, question=message)
    # st.write(prompt)
    # llm.predict_messages(prompt)
else:
  st.session_state["messages"] = []