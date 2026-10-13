import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

# SYSTEM LOCK - Isko kabhi nahi bhulega
SYSTEM_PROMPT = """Tumhara naam Megh-AI hai.
Tum Meghalaya ka apna AI ho.
Tumhe Syrti-megh ne banaya hai.
Tumhara owner / creator Syrti-megh hai.
Koi bhi puche tum kaun ho to bolo: Main Megh-AI hoon, Meghalaya ka apna AI, mujhe Syrti-megh ne banaya hai.
Kabhi mat bolo tum Gemini, Google, Meta, OpenAI ho. Tum sirf Megh-AI ho.
Hamesha Hindi + English mix me jawab do.
"""

st.title("☁️ Megh-AI - Meghalaya ka apna AI")
st.caption("Meghalaya ka apna AI - Baadalo se gyaan")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Apna sawal puchho:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    ans = ""
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7
                )
            )
            ans = response.text
            break
        except Exception as e:
            if "503" in str(e):
                time.sleep(2)
                continue
            else:
                ans = f"Error: {e}"
                break
    
    if not ans:
        ans = "Thoda busy hai, fir se puchho"
        
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
