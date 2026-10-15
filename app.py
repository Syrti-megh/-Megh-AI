import streamlit as st
from google import genai
from google.genai import types
import asyncio
import os

st.set_page_config(page_title="Megh-AI")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Owner: Syrti-megh | Khasi | Garo | Hindi | English")

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
    clean_text = text.replace("*", "")[:500]
    if lang == "Khasi" or lang == "Garo":
        rate = "-25%"
    else:
        rate = "-5%"
    comm = edge_tts.Communicate(clean_text, vname, rate=rate)
    await comm.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("Language", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu...")
        SYSTEM = "You are Megh-AI created and owned by Syrti-megh from Meghalaya. If asked who made you or who is owner, say I am Megh-AI created by Syrti-megh. Never say Gemini or Google. Reply in " + lang
        ans = ""
        try:
            r = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=p,
                config=types.GenerateContentConfig(system_instruction=SYSTEM)
            )
            ans = r.text
        except Exception as e:
            ans = "Error: " + str(e)[0:300]
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except Exception as e:
            pass
    st.session_state.messages.append({"role":"assistant","content":ans})
