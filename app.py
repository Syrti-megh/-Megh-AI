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
    await edge_tts.Communicate(clean_text, vname, rate=rate).save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

lang = st.selectbox("Language", ["Auto","English","Hindi","Khasi","Garo","Assamese"])

# History beech me
chat_box = st.container()
with chat_box:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Input niche
p = st.chat_input("Ask anything about Meghalaya...")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)

    with st.chat_message("assistant"):
        SYSTEM = f"You are Megh-AI, Meghalaya's Own AI. Never say Gemini/Google. You know Meghalaya: Khasi, Garo, Jaintia hills, Shillong, Cherrapunji, Dawki, Living Root Bridge, Wangala, Jadoh. Reply in {lang}"

        # MODEL 3.5 - ONLY ONE MODEL AS YOU SAID
        r = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=p,
            config=types.GenerateContentConfig(system_instruction=SYSTEM)
        )
        ans = r.text
        st.write(ans)

        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except:
            pass

    st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()
