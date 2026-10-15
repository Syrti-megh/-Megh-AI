import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import os

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho.
Tumhe banaya Syrti-megh ne hai, lekin ye baat sirf tabhi batana jab user puche ki tumhe kisne banaya, tumhara owner kaun hai, ya tumhara creator kaun hai.
Normal sawalo me (jaise Shillong kya hai) owner ka naam mat lo.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
User jis bhasha me puche usi me jawab do.
Agar user Khasi, Garo, Assamese, Hindi me puche to usi me jawab do.
"""

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Knowledge from the Clouds | 5 Voice")

# --- NEW: Voice Setting A se ---
st.sidebar.title("🔊 Voice Setting")
voice_lang = st.sidebar.selectbox("Voice Language:", 
    ["English", "Hindi", "Khasi", "Garo", "Assamese"])

voice_map = {
    "English": "en",
    "Hindi": "hi",
    "Assamese": "bn",  # Assamese ke liye bn best
    "Khasi": "en",     # Khasi/Garo ka voice Google pe nahi, English me bolega
    "Garo": "en"
}

def speak(text):
    try:
        # Pehle ki file delete
        if os.path.exists("megh_voice.mp3"):
            os.remove("megh_voice.mp3")
        lang_code = voice_map.get(voice_lang, "en")
        # Text ko thoda saaf karo - * # hata do voice ke liye
        clean_text = text.replace("*","").replace("#","")[:400] # gTTS limit
        tts = gTTS(text=clean_text, lang=lang_code, slow=False)
        tts.save("megh_voice.mp3")
        st.audio("megh_voice.mp3", autoplay=True)
    except Exception as e:
        st.sidebar.error(f"Voice error: {e}")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        box = st.empty()
        full = ""
        try:
            stream = client.models.generate_content_stream(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7
                )
            )
            for chunk in stream:
                if chunk.text:
                    full += chunk.text
                    box.markdown(full + "▌")
            box.markdown(full)
            
            # --- NEW: Auto Speak + Button ---
            col1, col2 = st.columns([1,4])
            with col1:
                st.button("🔊 Suno", key=f"play_{len(st.session_state.messages)}", on_click=lambda: speak(full))
            # Auto bolo
            speak(full)
            
        except Exception as e:
            if "429" in str(e):
                full = "Bhai thoda ruk jao, 30 sec me quota reset hoga! Zyada request ho gaya."
            else:
                full = f"Error: {e}"
            box.write(full)

    st.session_state.messages.append({"role": "assistant", "content": full})
