import streamlit as st
from db import create_usertable, add_user, login_user
import time
import dotenv
import os

# 載入 .env 檔案
dotenv.load_dotenv()

# 初始化 session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # 初始化登入狀態
if 'username' not in st.session_state:
    st.session_state.username = ""  # 儲存已登入的使用者名稱

if 'page_index' not in st.session_state:
    st.session_state.page_index = 0  # 預設頁面為登入頁面

# Sidebar 選單
with st.sidebar:
    # 如果使用者已登入，顯示帳號資訊
    if st.session_state.logged_in:
        st.write(f"已登入帳號：{st.session_state.username}")
        if st.button("登出"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page_index = 0
            st.rerun()  # 重新執行程式碼，更新狀態
    else:
        # 使用 index 來控制頁面狀態
        selected_page_index = st.selectbox(
            "選擇操作", ['login', 'register'], key='page_selector', index=st.session_state.page_index
        )
        st.session_state.page_index = 0 if selected_page_index == 'login' else 1

# 根據 page_index 顯示對應的頁面
if st.session_state.page_index == 1 and not st.session_state.logged_in:  # 註冊頁面
    st.subheader('註冊新帳號')

    new_user = st.text_input('使用者名稱', key='new_user')
    new_password = st.text_input('密碼', type='password', key='new_password')

    if st.button('註冊'):
        create_usertable()
        hashed_new_password = new_password
        add_user(new_user, hashed_new_password)
        st.success('註冊成功，正在跳轉至登入頁面...')
        time.sleep(2)  # 等待 2 秒
        # 修改頁面狀態為登入頁面
        st.session_state.page_index = 0
        st.rerun()  # 重新執行程式碼，更新頁面

elif st.session_state.page_index == 0 and not st.session_state.logged_in:  # 登錄頁面
    st.subheader('帳號登入')
    username = st.text_input('使用者名稱', key='login_user')
    password = st.text_input('密碼', type='password', key='login_password')
    if st.button('登入'):
        result = login_user(username, password)
        if result:
            st.success(f'歡迎，{username}')
            st.balloons()
            time.sleep(0.5)
            # 設置為已登錄並儲存使用者名稱
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.warning('使用者名稱或密碼錯誤')

# 登錄後的主頁面
if st.session_state.logged_in:
    st.subheader('主頁面')
    # 您的主頁面內容，例如聊天機器人
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
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

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
