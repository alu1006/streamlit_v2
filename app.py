import streamlit as st
from db import create_usertable, add_user, login_user
import time
import dotenv
import os

# 載入 .env 檔案
dotenv.load_dotenv()


# # 初始化 session state
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False  # 初始化登入狀態


# # Sidebar 選單
# with st.sidebar:
#     choice = st.selectbox(
#         "選擇操作", ['login', 'register']
#     )

# # 註冊頁面
# if choice == 'register':
#     st.subheader('註冊新帳號')

#     new_user = st.text_input('使用者名稱')
#     new_password = st.text_input('密碼')

#     if st.button('註冊'):
#         create_usertable()
#         hashed_new_password = new_password
#         add_user(new_user, hashed_new_password)
#         st.success('註冊成功，正在跳轉至登入頁面...')
#         time.sleep(2)  # 等待 2 秒
#         # 修改頁面狀態為登入頁面
        
# # 登錄頁面
# else:
#     st.subheader('帳號登入')
#     username = st.text_input('使用者名稱')
#     password = st.text_input('密碼', type='password')
#     if st.button('登入'):
#         result = login_user(username, password)
#         if result:
#             st.success(f'歡迎，{username}')
#             st.balloons()
#             time.sleep(0.5)
#             # 設置為已登錄
#             st.session_state.logged_in = True

            

#         else:
#             st.warning('使用者名稱或密碼錯誤')

# if st.session_state.logged_in:
import streamlit as st
from openai import OpenAI
api_key = os.getenv("OPENAI_KEY")
user_input = st.text_input("輸入對話:")

# 當使用者點擊 "送出" 按鈕時觸發
if st.button("送出"):
    # 顯示用戶訊息
    with st.chat_message("user"):
        st.write(user_input)

    # 設定聊天區域，用於顯示 GPT 回應
    with st.chat_message("assistant"):
        output_placeholder = st.empty()

        # 創建 OpenAI 客戶端
        client = OpenAI(api_key=api_key)
        print(client.models.list())
        # 呼叫 OpenAI API 並啟用串流模式
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            stream=True,
        )

        # 逐步顯示 GPT 回應
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                output_placeholder.markdown(full_response)
