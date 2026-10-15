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
    "Kokborok": "en-IN-PrabhatNeural",
    "Assamese": "bn-IN-BashkarNeural",
    "Auto": "en-US-GuyNeural"
}

async def make_voice(text, vname, lang):
    if os.path.exists("voice.mp3"): 
        os.remove("voice.mp3")
    import edge_tts
    clean_text = text.replace("*", "").replace("'", " ").replace("!", ".").replace("#", "")[:400]
    
    if lang in ["Khasi", "Garo", "Kokborok"]:
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

# --- NAYA MIC SYSTEM - BHEJO BUTTON WALA ---
st.divider()
st.write("🎤 **Step 1: Mic se bolo**")
audio_input = st.audio_input("Mic dabao aur bolo:")

user_prompt = None

if audio_input:
    st.write("✅ **Recording ho gayi! Ab sun lo:**")
    st.audio(audio_input)
    
    col1, col2 = st.columns(2)
    with col1:
        bhejo_btn = st.button("📤 BHEJO / SEND", type="primary", use_container_width=True)
    with col2:
        cancel_btn = st.button("❌ Cancel Karo", use_container_width=True)

    if cancel_btn:
        st.rerun()

    if bhejo_btn:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_input.getvalue())
            f_path = f.name
        
        with st.spinner("Samajh raha hu... Roman me likh raha hu..."):
            try:
                uploaded = client.files.upload(file=f_path)
                # --- ROMAN ENGLISH FIX ---
                r = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[f"Transcribe this audio in ROMAN ENGLISH ONLY. Use only A-Z English letters. NEVER use Devanagari/Hindi/Bengali script. Language is {lang}. If Garo, write Garo in Roman like 'Kumno nangni mung ma?':", uploaded]
                )
                user_prompt = r.text
                st.success(f"Samjha: {user_prompt}")
                os.remove(f_path)
                st.session_state["temp_prompt"] = user_prompt
            except Exception as e:
                st.error(f"Error: {e}")
                user_prompt = None

# Agar BHEJO se aaya hai to use karo
if "temp_prompt" in st.session_state and st.session_state["temp_prompt"]:
    user_prompt = st.session_state["temp_prompt"]
    st.session_state["temp_prompt"] = None

st.write("⌨️ **Step 2: Ya yahan likh ke bhejo**")
p = st.chat_input("Yahan likho... Garo / Khasi / Kokborok - Sab Roman me!")

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
        # --- FINAL ROMAN ENGLISH FIX ---
        SYSTEM_PROMPT = f"""You are Megh-AI, created by Syrti-megh from Meghalaya. You know 5 languages: Garo, Khasi, Kokborok, Hindi, English.
        CRITICAL RULES:
        1. ALWAYS reply in ROMAN ENGLISH ONLY. Use only A-Z English letters. NEVER EVER use Devanagari (ना, थी, मां), Bengali, or any other script. This is MANDATORY.
        2. If user speaks Hindi, write Hindi in Roman like 'Namaste! Mai Megh-AI hu. Kaise ho?' NOT 'नमस्ते'.
        3. If user speaks Garo, write Garo in Roman like 'Kumno? Nangni mung ma?' NOT in other script.
        4. Reply language is {lang} but script is ALWAYS Roman English.
        5. If asked who made you, say I am Megh-AI created by Syrti-megh. Never say Gemini or Google.
        Keep answer short for villagers."""
        
        ans = get_ai_response(user_prompt, SYSTEM_PROMPT)
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-US-GuyNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except: pass
    st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()
