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
OWNER: Jab puche to bolo Mere owner Syrti-megh hai / My owner is Syrti-megh.
LANGUAGE: User jis bhasha me puche usi me jawab do.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
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
            # Sabse tez + high quota model
            stream = client.models.generate_content_stream(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            for chunk in stream:
                if chunk.text:
                    full += chunk.text
                    box.markdown(full + "▌")
            box.markdown(full)
        except Exception as e:
            if "429" in str(e):
                full = "Thoda zyada traffic hai, 30 sec baad dubara pucho bhai! 🍞 App oven se nikla hai isliye."
            else:
                full = f"Error: {e}"
            box.write(full)

    st.session_state.messages.append({"role": "assistant", "content": full})
