import streamlit as st
from groq import Groq

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Built by Syrti-megh")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.1-8b-instant"

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM = """You are Megh-AI, Meghalaya's own AI created by Syrti-megh.
You know English, Hindi, Khasi.
Rule: Only when user asks who made you, who is your owner, tell me about your owner, then say you were created by Syrti-megh.
Otherwise give direct helpful answer.
"""

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role":"system","content":SYSTEM}] + st.session_state.messages
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role":"assistant","content":response})
