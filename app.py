import streamlit as st
from google import genai
from google.genai import types
import time, os, asyncio

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya | English • हिंदी • Khasi • Garo • Assamese")

# --- LANGUAGE SELECT ---
lang = st.selectbox("🌐 Language / Bhakha:", ["Auto (Same as you type)", "English", "Hindi", "Khasi", "Garo", "Assamese"], index=0)

# --- VOICE MAPPING ---
VOICE_MAP = {
    "English": "en-IN-PrabhatNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Khasi": "en-IN-PrabhatNeural", # Khasi voice not in edge-tts, English best clear
    "Garo": "en-IN-PrabhatNeural",
    "Assamese": "bn-IN-TanishaaNeural", # Assamese close to Bengali
    "Auto (Same as you type)": "hi-IN-MadhurNeural"
}

async def create_voice(text, voice_name):
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")
    clean = text.replace("*","").replace("#","").replace("_","")[:500]
    import edge_tts
    communicate = edge_tts.Communicate(clean, voice_name)
    await communicate.save("voice.mp3")
    return "voice.mp3"

def speak(text, selected_lang):
    try:
        voice_name = VOICE_MAP.get(selected_lang, "hi-IN-MadhurNeural")
        # Auto me Hindi text hai to Hindi voice, English hai to English voice
        if selected_lang == "Auto (Same as you type)":
            if any('\u0900' <= c <= '\u097F' for c in text): # Hindi
                voice_name = "hi-IN-MadhurNeural"
            else:
                voice_name = "en-IN-PrabhatNeural"
        
        file = asyncio.run(create_voice(text, voice_name))
        st.audio(file, autoplay=True)
    except Exception as e:
        pass

# --- SYSTEM PROMPT FOR ALL LANGUAGE ---
SYSTEM_PROMPT = f"""
You are Megh-AI, Meghalaya's Own AI. Made by Syrti-megh. Never say you are Gemini.

RULES:
1. You MUST reply in the same language user typed. You know 5 languages: English, Hindi (हिंदी), Khasi, Garo (A.chik), Assamese (অসমীয়া).
2. If user selected language is {lang} and it is not Auto, reply in {lang} only.
3. If language is Khasi, reply in Khasi. Example: Khublei, Kumno long?
4. If language is Garo, reply in Garo. Example: Indiba?
5. If language is Assamese, reply in Assamese.
6. Keep answer short and friendly.
"""

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

p = st.chat_input("Ask anything... Kuch bhi pucho... Phi ei...")
if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)

    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... ⏳")
        
        ans = None
        MODELS = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]
        
        for model_name in MODELS:
            try:
                r = client.models.generate_content(
                    model=model_name,
                    contents=p,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
                )
                ans = r.text
                break
            except:
                time.sleep(1)
                continue
        
        if not ans:
            ans = "Thoda busy hai, fir se bolo 🙏 / Thik se pucho"
        
        box.markdown(ans)
        speak(ans, lang)
    
    st.session_state.messages.append({"role":"assistant","content":ans})
