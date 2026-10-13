import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

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
    
    full_prompt = f"Tum Megh-AI ho, Meghalaya ka apna AI. Tumhe Syrti-megh ne banaya hai. Tumhara owner Syrti-megh hai. Kabhi mat bolo tum Google/Gemini ho. Sawal: {prompt}"
    
    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
    ans = ""
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(model=model_name, contents=full_prompt)
            ans = response.text
            break
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(1)
                continue
            else:
                ans = f"Error with {model_name}: {e}"
                continue
    
    if not ans:
        ans = "Server busy hai bhai, 1 minute baad try karo - 3.8-flash me bahut bheed hai abhi"
        
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
