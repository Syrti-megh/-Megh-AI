import streamlit as st
from google import genai
from google.genai import types
import os
import asyncio
import edge_tts

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho.
Tumhe banaya Syrti-megh ne hai.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
Jawab chota aur saaf rakho.
"""

st.title("☁️ Megh-AI")
st.caption("Model: gemini-3.8-flash")

# Ladka Clear Vocal
voice = "hi-IN-MadhurNeural"

async def make_voice(text):
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")
    clean = text.replace("*","").replace("#","")[:400]
    comm = edge_tts.Communicate(clean, voice)
    await comm.save("voice.mp3")
    return "voice.mp3"

def speak(text):
    file = asyncio.run(make_voice(text))
    if os.path.exists(file):
        st.audio(file, autoplay=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        try:
            # SIRF 3.8 FLASH
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )
            st.write(response.text)
            speak(response.text)
            ans = response.text
        except Exception as e:
            ans = f"Error: {e}"
            st.write(ans)

    st.session_state.messages.append({"role": "assistant", "content": ans})
