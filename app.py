import streamlit as st
from google import genai
from google.genai import types
import asyncio
import os

st.set_page_config(page_title="Megh-AI", layout="centered")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's Own AI | Khasi | Garo | Jaintia")

VOICE_MAN = {
    "English": "en-IN-PrabhatNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Khasi": "en-IN-PrabhatNeural",
    "Garo": "en-IN-PrabhatNeural",
    "Assamese": "bn-IN-BashkarNeural",
    "Auto": "en-IN-PrabhatNeural"
}

async def make_voice(text, vname, lang):
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")
    import edge_tts
    clean_text = text.replace("*", "")[:400]
    rate = "-25%" if lang in ["Khasi","Garo"] else "-5%"
    comm = edge_tts.Communicate(clean_text, vname, rate=rate)
    await comm.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

lang = st.selectbox("Language", ["Auto","English","Hindi","Khasi","Garo","Assamese"])

# --- CHAT HISTORY MIDDLE ME ---
chat_box = st.container()
with chat_box:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

# --- CHAT INPUT NICHE ---
p = st.chat_input("Ask anything about Meghalaya...")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    with chat_box:
        st.chat_message("user").write(p)

    with chat_box:
        with st.chat_message("assistant"):
            box = st.empty()
            box.markdown("Soch raha hu...")

            SYSTEM = f"""
            You are Megh-AI, Meghalaya's Own AI.
            Never say you are Gemini or Google.
            You have deep knowledge of Meghalaya: Khasi, Garo, Jaintia hills, Shillong, Sohra (Cherrapunji), Dawki, Living Root Bridges, Nohkalikai, Mawlynnong, Wangala, Shad Suk Mynsiem, Behdienkhlam, Jadoh, Dohneiiong, Tungrymbai.
            If asked who you are, say: I am Megh-AI, Meghalaya's Own AI.
            Reply in {lang} if not Auto.
            """

            # ONLY ONE MODEL - 3.5 wala
            r = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=p,
                config=types.GenerateContentConfig(system_instruction=SYSTEM)
            )
            ans = r.text
            box.markdown(ans)

            try:
                vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
                f = asyncio.run(make_voice(ans, vname, lang))
                st.audio(f, autoplay=True)
            except:
                pass

    st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()
