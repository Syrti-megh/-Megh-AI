import streamlit as st
from google import genai
from google.genai import types
import os
import asyncio
import edge_tts
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho.
Tumhe banaya Syrti-megh ne hai, lekin ye baat sirf tabhi batana jab user puche ki tumhe kisne banaya, tumhara owner kaun hai, ya tumhara creator kaun hai.
Normal sawalo me owner ka naam mat lo.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
User jis bhasha me puche usi me jawab do.
Jawab chota aur saaf rakho, 4-5 line me.
"""

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Boy Voice | Clear Vocal")

st.sidebar.title("🔊 Voice Setting")
voice_lang = st.sidebar.selectbox("Voice Language:", ["Hindi", "English", "Khasi", "Garo", "Assamese"])

voice_map = {
    "Hindi": "hi-IN-MadhurNeural",
    "English": "en-IN-PrabhatNeural",
    "Assamese": "hi-IN-MadhurNeural",
    "Khasi": "en-IN-PrabhatNeural",
    "Garo": "en-IN-PrabhatNeural"
}

async def generate_voice(text, lang):
    try:
        if os.path.exists("megh_voice.mp3"):
            os.remove("megh_voice.mp3")
        clean_text = text.replace("*","").replace("#","").replace("_","")[:500]
        voice = voice_map.get(lang, "hi-IN-MadhurNeural")
        communicate = edge_tts.Communicate(clean_text, voice)
        await communicate.save("megh_voice.mp3")
        return "megh_voice.mp3"
    except:
        return None

def speak(text):
    file = asyncio.run(generate_voice(text, voice_lang))
    if file and os.path.exists(file):
        st.audio(file, autoplay=True)

# --- MAIN LOGIC WITH FALLBACK ---
def get_ai_response(prompt):
    models_to_try = ["gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-flash-latest", "gemini-3.8-flash"]
    for model_name in models_to_try:
        try:
            stream = client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
            )
            full_text = ""
            for chunk in stream:
                if chunk.text:
                    full_text += chunk.text
            if full_text:
                return full_text, model_name
        except Exception as e:
            if "503" in str(e) or "404" in str(e) or "429" in str(e):
                time.sleep(1)
                continue
            else:
                continue
    return "Bhai server busy hai, 10 sec baad fir se try karo!", "none"

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
        box.markdown("Soch raha hu... ⏳")
        response, used_model = get_ai_response(prompt)
        box.markdown(response)
        st.caption(f"Model: {used_model}")
        speak(response)
        full = response
    st.session_state.messages.append({"role": "assistant", "content": full})
