import streamlit as st
from google import genai
from google.genai import types
import asyncio
import os

st.set_page_config(page_title="Megh-AI")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's Own AI | Khasi | Garo | Jaintia | Hindi | English")

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

lang = st.selectbox("Choose Language", ["Auto","English","Hindi","Khasi","Garo","Assamese"])

# YEH NAYA HAI - ab chat_input ki jagah text_input
p = st.text_input("Yahan likho...", placeholder="Ask anything about Meghalaya...")
btn = st.button("Send 🚀")

# Purane messages dikhao
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if btn and p:
    st.session_state.messages.append({"role":"user","content":p})
    with st.chat_message("user"):
        st.write(p)
    
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu...")

        SYSTEM = """
        You are Megh-AI, Meghalaya's Own AI.
        Never say you are Gemini or Google.
        You have deep knowledge of Meghalaya: Khasi, Garo, Jaintia hills, Shillong, Cherrapunji, Dawki, Living Root Bridges, Wangala, Shad Suk Mynsiem, Jadoh, Dohneiiong.
        If asked who you are, say: I am Megh-AI, Meghalaya's Own AI.
        Reply in """ + lang

        try:
            r = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=p,
                config=types.GenerateContentConfig(system_instruction=SYSTEM)
            )
            ans = r.text
        except Exception as e:
            ans = "Error: " + str(e)[0:400]
        
        box.markdown(ans)

        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except:
            pass
            
    st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()
