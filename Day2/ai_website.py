import time
import os
import joblib as jl
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from streamlit import session_state

load_dotenv()
GOOGLE_API_KEY = 'AIzaSyC5KfQjhYGIbSLBfNLhurGLTNGtpEfIrFc'
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f"{time.time()}"
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🌀'

if not os.path.exists('../Day1/data'):
    os.mkdir('../data')

try:
    past_chats = jl.load('../Day1/data/past-chats-list')
except:
    past_chats = {}

with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x,'New Chat'),
            placeholder='_'
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x:past_chats.get(x,'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_'
        )
    st.session_state.chat_title = f"ChatSession-{st.session_state.chat_id}"

st.write('# Chat with BLACKHOLE 🌀')

try:
    st.session_state.messages = jl.load(f"../Day1/data/{st.session_state.chat_id}-st_messages")
    st.session_state.gemini_history = jl.load(f"../Day1/data{st.session_state.chat_id}-gemini_messages")
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []

st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

if prompt := st.chat_input("Type Something..."):
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        jl.dump(past_chats, '../Day1/data/past-chats-list')

    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append(dict(role='user', content=prompt))

    response = st.session_state.chat.send_message(prompt, stream=True)
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        message_placeholder = st.empty()
        full_response = ''
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response + ' ')
        message_placeholder.write(full_response)


    st.session_state.messages.append(dict(role=MODEL_ROLE, content=full_response, avatar=AI_AVATAR_ICON))
    st.session_state.gemini_history = st.session_state.chat.history

    jl.dump(st.session_state.messages, f'../Day1/data/{st.session_state.chat_id}-st_messages')
    jl.dump(st.session_state.gemini_history, f'../Day1/data/{st.session_state.chat_id}-gemini_messages')