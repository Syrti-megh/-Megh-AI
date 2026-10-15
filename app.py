import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | English • हिंदी • Khasi • Garo • Assamese")

VOICE_MAN = {"English":"en-IN-PrabhatNeural","Hindi":"hi-IN-MadhurNeural","Khasi":"en-IN-PrabhatNeural","Garo":"en-IN-PrabhatNeural","Assamese":"bn-IN-BashkarNeural","Auto":"en-IN-PrabhatNeural"}

async def make_voice(text, vname):
    if os.path.exists("voice.mp3"): os.remove("voice.mp3")
    import edge_tts
    await edge_tts.Communicate(text.replace("*","")[:500], vname).save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages: st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("🗣️ Language:", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything...")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... ⏳")
        SYSTEM = f"You are Megh-AI by Syrti-megh. Never say Gemini. Reply in {lang} if not Auto else same as user. Know English, Hindi, Khasi, Garo, Assamese."
        ans = None
        try:
            # Sirf ek baar try - quota bachega
            r = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=p,
                config=types.GenerateContentConfig(system_instruction=SYSTEM)
            )
            ans = r.text
        except Exception as e:
            err = str(e)
            if "429" in err:
                ans = "🙏 Free quota khatam ho gaya hai! 1 minute ruk jao, fir se pucho. Ya [ai.google.dev](https://aistudio.google.com/app/apikey) pe jaake naya API key banao."
                st.error("429 Quota Exhausted - 1 min wait karo")
            else:
                ans = f"Error: {err[:300]}"
        
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname))
            st.audio(f, autoplay=True)
        except: pass
    st.session_state.messages.append({"role":"assistant","content":ans})
