import time
import streamlit as st

# 페이지 설정을 지정합니다. 페이지 제목과 아이콘을 설정합니다.
st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)

# 페이지의 제목을 설정합니다.
st.title("DocumentGPT")

# 세션 상태에 'messages'라는 키가 없으면 빈 리스트로 초기화합니다.
# 이는 이미 메시지가 있는 경우 세션 상태를 유지하기 위함입니다.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 메시지를 보내는 함수 정의
# 메시지 내용, 역할, 저장 여부를 인자로 받습니다.
def send_message(message, role, save=True):
    # 주어진 역할에 따라 채팅 메시지를 출력합니다.
    with st.chat_message(role):
        st.write(message)
    # save가 True인 경우, 메시지를 세션 상태에 저장합니다.
    if save:
        st.session_state["messages"].append({"message": message, "role": role})

# 세션 상태에 저장된 모든 메시지를 화면에 출력합니다.
# 저장된 메시지를 반복하며 send_message 함수를 호출하되, save=False로 설정하여 중복 저장을 방지합니다.
for message in st.session_state["messages"]:
    send_message(message["message"], message["role"], save=False)

# 사용자 입력을 받을 수 있는 채팅 입력창을 생성합니다.
message = st.chat_input("Send a message to the ai")

# 사용자가 메시지를 입력한 경우
if message:
    # 사용자의 메시지를 화면에 출력하고 세션 상태에 저장합니다.
    send_message(message, "human")
    # 응답을 생성하기 전에 2초간 대기합니다.
    time.sleep(2)
    # AI의 응답 메시지를 화면에 출력하고 세션 상태에 저장합니다.
    send_message(f"You said: {message}", "ai")
  
    # 사이드바에 세션 상태의 내용을 출력합니다.
    with st.sidebar:
        st.write(st.session_state)