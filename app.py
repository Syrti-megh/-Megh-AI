import streamlit as st
from google import genai
from google.genai import types

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
3. OWNER: Jab koi puche owner kaun hai, tumhara malik kaun hai, who is your owner, toh hi batana:
   - Hindi: Mere owner ka naam Syrti-megh hai, unhone mujhe banaya hai.
   - English: My owner is Syrti-megh, he created me.
   - Khasi: U trai jong nga u dei u Syrti-megh, u la thaw ia nga.
   Warna normal baat karo, owner ka naam har jagah mat dikhao.
"""

st.title("☁️ Megh-AI")
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
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
        )
        ans = response.text
    except:
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
            )
            ans = response.text
        except Exception as e:
            ans = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
