import streamlit as st
from google import genai

st.set_page_config(page_title="Megh-AI")
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI - Meghalaya ka apna AI")
st.caption("Meghalaya ka apna AI - Baadalo se bhi tez")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Apna sawal puchho:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    ans = response.text
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.chat_message("assistant").write(ans)
