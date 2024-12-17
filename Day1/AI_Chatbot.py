# API = "AIzaSyC5KfQjhYGIbSLBfNLhurGLTNGtpEfIrFc"
import time # This is to give timestamps to the API and localfiles
import os # This library giving us basic commands to CLI level user
import joblib as jl # Create a jobtask like make files or input something into a specific file
import google.generativeai as genai # SDK (Software Development Kit) supporting files for Gemini API
from dotenv import load_dotenv # .env library support to make API usage more stable
from colorama import Fore

# 1. Introduction Step
print("Hello! welcome to Blackhole. I come from a star and born into a blackhole!")
print("You can ask me anything because I swallow a lot of knowledge!\n")

# 2. Setting up bot
print("Before you access my knowledge please input your API below")
GOOGLE_API_KEY = input("Input your API Key : ") # This will save API to a local variable
print("\nSetting up Blackhole engine (Powered by Gemini).. ")
load_dotenv()
os.system("pause")

# 3. Checking API Connection to Google AI Studio
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    print("Conducting rerouting another API...")
    os.system("pause")
if not GOOGLE_API_KEY:
    print("Error! API Key not found, restart or check it in `.env` manually")
    os.system("pause")
    exit(1)

# 4. Configure Gemini as our chat-bot
genai.configure(api_key=GOOGLE_API_KEY)
print("Blackhole engine(Gemini powered) is activated!")

# 5. Creating unique chat session!
chat_title = input("Enter a name for your chat session (Default = 'Alien')") or "Alien"
new_chat_id = f"{time.time()}"

# 6. backlog
if not os.path.exists('data/'): # checking if the folder existed or not
    os.mkdir('data/') # if not then make 1

# Try to load previous chat if available
try:
    past_chats = jl.load('data/past_chats_list')
    print("\nPrevious chat session loaded successfully")
except FileNotFoundError:
    past_chats = {}
    print("\nNo previous chat sessions found. Starting Fresh..")

# Initialize the chatbot model
print("Initializing Blackhole platform...")
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()
print("Blackhole Platform is Initialized!")
try:
    messages = jl.load(f"data/{new_chat_id}-messages")
except FileNotFoundError:
    messages = []
if new_chat_id not in past_chats:
    past_chats[new_chat_id] = chat_title
    jl.dump(past_chats, 'data/past-chats-list')

# 7. Start the chat session!
print("\nYour blackhole platform is created, let's start discussing!")
print("type `exit` to quit.")

# 8. Loop the chat and give conditions
while True:
    print(Fore.BLUE)
    user_input = input(f"{chat_title} (You) : ")
    if user_input.lower() == 'exit':
        print("You are leaving the blackhole platform, goodbye!")
        break

    response = chat.send_message(user_input)
    print(Fore.RED)
    print(f"BLACKHOLE : {response.text}")

    messages.append({'role' : 'user', 'content':user_input})
    messages.append({'role' : 'ai', 'content':response.text})
    jl.dump(messages,f"data/{new_chat_id}-messages")
    print("Chat history saved!")