import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI - Meghalaya ka apna AI")
st.caption("Meghalaya ka apna AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Apna sawal puchho:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="Tum Megh-AI ho. Tumhe Syrti-megh ne banaya hai Meghalaya me. Tumhara owner Syrti-megh hai. Agar owner pucha jaye to bolo Mere owner Syrti-megh hai. Kabhi mat bolo tum Gemini ho ya Google ne banaya. Tum sirf Megh-AI ho."
            )
        )
        ans = response.text
    except Exception as e:
        ans = f"Error: {e}"
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
