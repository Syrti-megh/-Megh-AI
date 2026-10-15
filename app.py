import streamlit as st
from google import genai
from google.genai import types
import os
import asyncio
import edge_tts

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
Jawab chota aur saaf rakho, 4-5 line me.
"""

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Knowledge from the Clouds | 5 Voice CLEAR")

# --- CLEAR VOICE SETTING ---
st.sidebar.title("🔊 Clear Voice Setting")
voice_lang = st.sidebar.selectbox("Voice Language:", 
    ["Hindi", "English", "Khasi", "Garo", "Assamese"])

# Microsoft ki sabse clear voice
voice_map = {
    "Hindi": "hi-IN-SwaraNeural",      # Ekdum clear Hindi
    "English": "en-IN-NeerjaNeural",   # Indian English
    "Assamese": "en-IN-NeerjaNeural",  # Assamese clear
    "Khasi": "en-IN-NeerjaNeural",     # Khasi/Garo English accent me saaf
    "Garo": "en-IN-NeerjaNeural"
}

async def generate_voice(text, lang):
    try:
        if os.path.exists("megh_voice.mp3"):
            os.remove("megh_voice.mp3")
        clean_text = text.replace("*","").replace("#","").replace("_","")[:500]
        voice = voice_map.get(lang, "hi-IN-SwaraNeural")
        communicate = edge_tts.Communicate(clean_text, voice)
        await communicate.save("megh_voice.mp3")
        return "megh_voice.mp3"
    except Exception as e:
        st.error(f"Voice error: {e}")
        return None

def speak(text):
    file = asyncio.run(generate_voice(text, voice_lang))
    if file and os.path.exists(file):
        st.audio(file, autoplay=True)

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
            
            # Suno Button + Auto Speak
            if st.button("🔊 Suno", key=f"play_{len(st.session_state.messages)}"):
                speak(full)
            
            # Auto bolo
            speak(full)
            
        except Exception as e:
            if "429" in str(e):
                full = "Bhai thoda ruk jao, 30 sec me quota reset hoga!"
            else:
                full = f"Error: {e}"
            box.write(full)

    st.session_state.messages.append({"role": "assistant", "content": full})
