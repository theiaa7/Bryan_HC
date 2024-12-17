import time
import os
import joblib as jl
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = "AIzaSyC5KfQjhYGIbSLBfNLhurGLTNGtpEfIrFc"
if GOOGLE_API_KEY is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f"{time.time()}"
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '🌀'

# Ensure data directory exists
data_dir = '../Day1/data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Initialize past chats if not found
past_chats_file = os.path.join(data_dir, 'past-chats-list')
if not os.path.exists(past_chats_file):
    past_chats = {}
    jl.dump(past_chats, past_chats_file)
else:
    past_chats = jl.load(past_chats_file)

# Sidebar for selecting past chats
with st.sidebar:
    st.write('# Past Chats')
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_'
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_'
        )
    st.session_state.chat_title = f"ChatSession-{st.session_state.chat_id}"

st.write('# Chat with BLACKHOLE 🌀')

# Initialize messages and history if not found
messages_file = os.path.join(data_dir, f"{st.session_state.chat_id}-st_messages")
gemini_history_file = os.path.join(data_dir, f"{st.session_state.chat_id}-gemini_messages")

if not os.path.exists(messages_file):
    st.session_state.messages = []
    jl.dump(st.session_state.messages, messages_file)
else:
    st.session_state.messages = jl.load(messages_file)

if not os.path.exists(gemini_history_file):
    st.session_state.gemini_history = []
    jl.dump(st.session_state.gemini_history, gemini_history_file)
else:
    st.session_state.gemini_history = jl.load(gemini_history_file)

# Initialize the AI model
st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# User input handling
if prompt := st.chat_input("Type Something..."):
    # Update past chats if this is a new chat
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        jl.dump(past_chats, past_chats_file)

    # Display user message
    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append(dict(role='user', content=prompt))

    # Get AI response
    response = st.session_state.chat.send_message(prompt, stream=True)
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        message_placeholder = st.empty()
        full_response = ''
        for chunk in response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)  # Simulate typing delay
                message_placeholder.write(full_response + ' ')
        message_placeholder.write(full_response)

    # Store AI response and update history
    st.session_state.messages.append(dict(role=MODEL_ROLE, content=full_response, avatar=AI_AVATAR_ICON))
    st.session_state.gemini_history = st.session_state.chat.history

    # Save messages and history
    jl.dump(st.session_state.messages, messages_file)
    jl.dump(st.session_state.gemini_history, gemini_history_file)