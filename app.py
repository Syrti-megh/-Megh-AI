import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
st.title("☁️ Megh-AI")
st.caption("Meghalaya ka apna AI - Baadalon se bhi tez")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets me API Key daalo!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM = "You are Megh-AI from Umsning, Meghalaya. Friendly, Hindi English Khasi mix."

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Apna sawal puchho:"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hai..."):
            r = model.generate_content(SYSTEM + "\nUser:" + prompt)
            st.markdown(r.text)
            st.session_state.messages.append({"role":"assistant","content":r.text})
