import streamlit as st
from google import genai
from google.genai import types
import asyncio, os

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya | English • हिंदी • Khasi • Garo • Assamese")

# --- SIRF MAN VOICE ---
VOICE_MAN = {
    "English": "en-IN-PrabhatNeural",      # Indian Man - English
    "Hindi": "hi-IN-MadhurNeural",         # Indian Man - Hindi
    "Khasi": "en-IN-PrabhatNeural",        # Man - Khasi ke liye best
    "Garo": "en-IN-PrabhatNeural",         # Man - Garo ke liye
    "Assamese": "bn-IN-BashkarNeural",     # Man - Assamese/Bengali Man
    "Auto": "hi-IN-MadhurNeural"
}

async def make_voice_file(text, voice_name):
    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")
    clean = text.replace("*","").replace("#","").replace("_","")[:600]
    import edge_tts
    comm = edge_tts.Communicate(clean, voice_name)
    await comm.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("🗣️ Voice Language:", ["Auto", "English", "Hindi", "Khasi", "Garo", "Assamese"])

p = st.chat_input("Ask anything...")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)

    with st.chat_message("assistant"):
        try:
            SYSTEM = f"You are Megh-AI, Meghalaya's Own AI by Syrti-megh. Reply in {lang} if not Auto, else same as user language. You know English, Hindi, Khasi, Garo, Assamese. Never say Gemini."
            
            # 100% working model
            r = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=p,
                config=types.GenerateContentConfig(system_instruction=SYSTEM)
            )
            ans = r.text
            st.write(ans)

            # --- MAN VOICE PLAY ---
            try:
                v_name = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
                if lang == "Auto":
                    if any('\u0980' <= c <= '\u09FF' for c in ans): # Bengali/Assamese script
                        v_name = "bn-IN-BashkarNeural"
                    elif any('\u0900' <= c <= '\u097F' for c in ans): # Hindi
                        v_name = "hi-IN-MadhurNeural"
                    else:
                        v_name = "en-IN-PrabhatNeural"

                f = asyncio.run(make_voice_file(ans, v_name))
                st.audio(f, autoplay=True)
            except Exception as ve:
                st.caption(f"Voice error: {ve}")

        except Exception as e:
            st.error(f"Error: {e}")
            ans = f"Error: {e}"

    st.session_state.messages.append({"role":"assistant","content":ans})
