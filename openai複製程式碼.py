import streamlit as st
from db import create_usertable, add_user, login_user
import time
import dotenv
import os

# 載入 .env 檔案
dotenv.load_dotenv()

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
