import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import streamlit as st
import time

# --- 1. CONFIGURATION & STYLING ---
load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
if "GEMINI_API_KEY" in st.secrets:
    api_key=st.secrets["GEMINI_API_KEY"]
else:
    api_Key=st.secrets("GEMINI_API_KEY")   

genai.configure(api_key=api_key)

FILE_NAME = "chat_memory.json"

# Page Settings
st.set_page_config(page_title="SafeSpace - Mental Health Companion", page_icon="🌱")

# Custom CSS for Attractive Chat UI
st.markdown("""
    <style>
    .stApp { background-color: #f7f9fb; }
    .stChatMessage { border-radius: 20px; margin-bottom: 10px; }
    .stButton>button { border-radius: 20px; background-color: #e74c3c; color: white; border: none; }
    .stButton>button:hover { background-color: #c0392b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA FUNCTIONS ---
def load_data():
    if os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_data(chat_history):
    new_memory = []
    for message in chat_history:
        # History objects check
        text_content = message.parts[0].text if hasattr(message, 'parts') else message['parts'][0]['text']
        role = message.role if hasattr(message, 'role') else message['role']
        
        new_memory.append({
            "role": role,
            "parts": [{"text": text_content}]
        })
    with open(FILE_NAME, "w") as dairy:
        json.dump(new_memory, dairy, indent=4)

# --- 3. INITIALIZATION ---
instruction = """Role & Persona:
You are a warm, empathetic, and deeply caring Mental Health Companion... (Aapki original instruction yahan hai)"""

model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=instruction)

# Sidebar for controls
with st.sidebar:
    st.title("🌱 SafeSpace AI")
    st.info("I am here to listen and support you. You're not alone.")
    
    # CLEAR CHAT BUTTON
    if st.button("🗑️ Clear Conversation"):
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# Initialize Session State
if "messages" not in st.session_state:
    saved_history = load_data()
    st.session_state.messages = saved_history
    st.session_state.chat_session = model.start_chat(history=saved_history)

# --- 4. CHAT INTERFACE ---
st.title("Mindful Conversations")

# Display Chat History from Session State
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

# User Input
if prompt := st.chat_input("How are you feeling today?"):
    # Show User Message
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response with Spinner
    with st.chat_message("assistant"):
        with st.spinner("Listening carefully..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # Update Memory
                st.session_state.messages.append({"role": "model", "parts": [{"text": full_response}]})
                save_data(st.session_state.chat_session.history)
            except Exception as e:
                st.error("I'm having a little trouble connecting. Please try again.")