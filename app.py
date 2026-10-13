import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho.
Tumhe banaya Syrti-megh ne hai, lekin ye baat sirf tabhi batana jab user puche ki tumhe kisne banaya, tumhara owner kaun hai, ya tumhara creator kaun hai.
Normal sawalo me (jaise Shillong kya hai) owner ka naam mat lo.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
User jis bhasha me puche usi me jawab do.
"""

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Knowledge from the Clouds")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        box = st.empty()
        full = ""
        try:
            # Google ka latest model - 3.5-flash-lite
            stream = client.models.generate_content_stream(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7
                )
            )
            for chunk in stream:
                if chunk.text:
                    full += chunk.text
