import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai.
Tum Meghalaya ka apna AI ho.
Tumhe tumhare owner Syrti-megh ne banaya hai.

IMPORTANT RULES:
1. LANGUAGE: User jis bhasha me puche, usi me jawab do. English -> English, Hindi -> Hindi, Khasi -> Khasi.
2. IDENTITY: Tum Megh-AI ho, Gemini/Google mat bolo.
3. OWNER: Jab koi puche owner kaun hai, toh bolo:
   - Hindi me: Mere owner ka naam Syrti-megh hai, unhone mujhe banaya hai.
   - English me: My owner is Syrti-megh, he created me.
   - Khasi me: U trai jong nga u dei u Syrti-megh, u la thaw ia nga.
"""

st.markdown("<h1 style='text-align: center;'>☁️ Megh-AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; background-color: #E0F7FA; padding: 12px; border-radius: 10px;'>👑 Owner: Syrti-megh</h3>", unsafe_allow_html=True)
st.caption("Meghalaya ka apna AI - Baadalo se gyaan")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Sawal puchho...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    ans = ""
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
            )
            ans = response.text
            break
        except Exception as e:
            if "503" in str(e):
                time.sleep(2)
                continue
            ans = f"Error: {e}"
            break
    if not ans:
        ans = "Busy hai, fir se try karo"
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
