import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time, tempfile

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's FIRST 5 Language AI | Better than Lemka")

# 5 LANGUAGE - VOCAL MAN VOICE
VOICE_MAN = {
    "English": "en-US-GuyNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Khasi": "en-US-GuyNeural",
    "Garo": "en-US-GuyNeural",
    "Kokborok": "en-IN-PrabhatNeural", # Tripura ke liye
    "Assamese": "bn-IN-BashkarNeural",
    "Auto": "en-US-GuyNeural"
}

async def make_voice(text, vname, lang):
    if os.path.exists("voice.mp3"): 
        os.remove("voice.mp3")
    import edge_tts
    clean_text = text.replace("*", "").replace("'", " ").replace("!", ".").replace("#", "")[:400]
    
    if lang in ["Khasi", "Garo", "Kokborok"]:
        vname = "en-US-GuyNeural"
        rate = "-25%"
        volume = "+25%"
        pitch = "+4Hz"
        clean_text = clean_text.replace("Khublei", "Khoob Lay")
        clean_text = clean_text.replace("Nga dei", "Nga Day")
    else:
        rate = "-10%"
        volume = "+10%"
        pitch = "+0Hz"
    
    communicate = edge_tts.Communicate(clean_text, vname, rate=rate, volume=volume, pitch=pitch)
    await communicate.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

# --- 5 LANGUAGE SELECTOR ---
lang = st.selectbox("🌐 Language Chunlo:", ["Auto","English","Hindi","Khasi","Garo","Kokborok"])

# --- MIC + TEXT DONO ---
st.write("🎤 **Mic se bolo ya likho:**")
audio_input = st.audio_input("Mic dabao aur bolo:")

p = st.chat_input("Ya yahan likho... Garo / Khasi / Kokborok")

# Audio ko text me badlo
user_prompt = None
if audio_input:
    # Gemini se hi voice samjhega
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_input.getvalue())
        f_path = f.name
    
    st.chat_message("user").write("🎤 Voice bheja...")
    # Gemini audio transcription
    try:
        uploaded = client.files.upload(file=f_path)
        r = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=["Is audio ko text me likh do:", uploaded]
        )
        user_prompt = r.text
        st.success(f"Samjha: {user_prompt}")
    except:
        user_prompt = "Khublei"

if p:
    user_prompt = p

def get_ai_response(prompt_text, system_prompt):
    models_to_try = ["gemini-3.5-flash", "gemini-2.0-flash", "gemini-3.5-flash-lite"]
    for attempt in range(3):
        model_name = models_to_try[attempt % len(models_to_try)]
        try:
            r = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    thinking_config=types.ThinkingConfig(thinking_level="low")
                )
            )
            if r.text: return r.text
        except Exception as e:
            time.sleep(2)
            continue
    return "Mitela! Server busy hai, 1 min baad try kar!"

if user_prompt:
    st.session_state.messages.append({"role":"user","content":user_prompt})
    st.chat_message("user").write(user_prompt)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu...")
        SYSTEM_PROMPT = f"You are Megh-AI, created by Syrti-megh from Meghalaya. You know 5 languages: Garo, Khasi, Kokborok, Hindi, English. If asked who made you, say I am Megh-AI created by Syrti-megh. Never say Gemini or Google. Reply in {lang} language. If Auto, detect user language. Keep answer short for villagers."
        ans = get_ai_response(user_prompt, SYSTEM_PROMPT)
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-US-GuyNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except: pass
    st.session_state.messages.append({"role":"assistant","content":ans})
