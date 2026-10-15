import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya")

# --- MAN VOICE ONLY ---
VOICE_MAN = {
    "English": "en-IN-PrabhatNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Khasi": "en-IN-PrabhatNeural",
    "Garo": "en-IN-PrabhatNeural",
    "Assamese": "bn-IN-BashkarNeural",
    "Auto": "en-IN-PrabhatNeural"
}

async def make_voice(text, vname):
    if os.path.exists("voice.mp3"): os.remove("voice.mp3")
    clean = text.replace("*","").replace("#","")[:600]
    import edge_tts
    await edge_tts.Communicate(clean, vname).save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("🗣️ Language:", ["Auto", "English", "Hindi", "Khasi", "Garo", "Assamese"])

p = st.chat_input("Ask anything...")
if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)

    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... ⏳")
        
        SYSTEM = f"You are Megh-AI, Meghalaya's Own AI by Syrti-megh. Never say Gemini. Reply in {lang} if not Auto else same as user typed. You know English, Hindi, Khasi, Garo, Assamese."
        
        ans = None
        last_err = ""
        # 3.8 kabhi kabhi 503 deta hai, isliye 5 baar retry
        for i in range(5):
            try:
                r = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=p,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM)
                )
                ans = r.text
                break
            except Exception as e:
                last_err = str(e)
                if "503" in last_err or "overloaded" in last_err.lower():
                    time.sleep(2) # 2 sec ruk ke fir try
                    continue
                else:
                    break
        
        if not ans:
            st.error(f"Google busy hai (503), 10 sec baad try karo. Details: {last_err[:200]}")
            ans = "Server busy hai, 10 sec baad fir pucho 🙏"

        box.markdown(ans)
        
        try:
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname))
            st.audio(f, autoplay=True)
        except: pass

    st.session_state.messages.append({"role":"assistant","content":ans})
