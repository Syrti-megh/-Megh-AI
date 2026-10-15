import streamlit as st
from google import genai
from google.genai import types
import asyncio
import os
import time

st.set_page_config(page_title="Megh-AI", page_icon=":cloud:")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's FIRST Garo + Khasi AI | Better than Lemka")

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
    rate = "-35%" if lang in ["Khasi","Garo"] else "-10%"
    volume = "+10%" if lang in ["Khasi","Garo"] else "+0%"
    communicate = edge_tts.Communicate(clean_text, vname, rate=rate, volume=volume)
    await communicate.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("Language:", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything in Garo or Khasi...")

def get_ai_response(prompt_text, system_prompt):
    # 3.5 ka quota kam hai, isliye 1.5 pehle - 503 kabhi nahi aayega
    models_to_try = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-flash-8b"]
    for model_name in models_to_try:
        try:
            r = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            return r.text
        except Exception as e:
            time.sleep(0.5)
            continue
    return "Mitela! Server busy hai, 10 sec baad try karo! / Khublei!"

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu...")
        SYSTEM_PROMPT = (
            "You are Megh-AI, created and owned by Syrti-megh from Meghalaya. "
            "You are BETTER than Lemka because Lemka only knows Khasi, but YOU know Garo + Khasi + Pnar + English + Hindi. "
            "If asked who made you: Always say I am Megh-AI created by Syrti-megh from Meghalaya. "
            "Never say Gemini or Google or Meta. "
            "You are the FIRST AI to speak Garo fluently. "
            "GARO: Nameng=Hello, Nia dong=How are you, Mitela=Thank you. "
            "KHASI: Khublei, Kumno long. "
            f"Reply in {lang} if not Auto."
        )
        ans = get_ai_response(p, SYSTEM_PROMPT)
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except:
            pass
    st.session_state.messages.append({"role":"assistant","content":ans})
