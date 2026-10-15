import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time, tempfile

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's FIRST 5 Language AI | Bolke bhi sunata hai!")

VOICE_MAN = {
    "English": "en-US-GuyNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Khasi": "en-US-GuyNeural",
    "Garo": "en-US-GuyNeural",
    "Kokborok": "en-IN-PrabhatNeural",
    "Assamese": "bn-IN-BashkarNeural",
    "Auto": "en-US-GuyNeural"
}

# AI BOLEGA - VOICE FUNCTION
async def make_voice(text, vname, lang):
    try:
        if os.path.exists("voice.mp3"):
            os.remove("voice.mp3")
        import edge_tts
        # Clean text for voice
        clean_text = text.replace("*", "").replace("'", " ").replace("!", ".").replace("#", "").replace("_", "")[:450]
        rate = "-20%" if lang in ["Khasi", "Garo", "Kokborok"] else "-10%"
        volume = "+20%"
        pitch = "+2Hz"
        communicate = edge_tts.Communicate(clean_text, vname, rate=rate, volume=volume, pitch=pitch)
        await communicate.save("voice.mp3")
        return "voice.mp3"
    except Exception as e:
        print(f"Voice error: {e}")
        return None

if "messages" not in st.session_state:
    st.session_state.messages = []
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("🌐 Language Chunlo:", ["Auto","English","Hindi","Khasi","Garo","Kokborok"])

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
                models_voice = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
                for m_name in models_voice:
                    try:
                        r = client.models.generate_content(
                            model=m_name,
                            contents=[f"Transcribe this audio in ROMAN ENGLISH ONLY. Only A-Z letters. NEVER Devanagari. Language is {lang}:", uploaded]
                        )
                        if r.text:
                            user_prompt = r.text
                            break
                    except:
                        continue
                st.success(f"Samjha: {user_prompt}")
                os.remove(f_path)
                st.session_state["temp_prompt"] = user_prompt
            except Exception as e:
                st.error(f"Error: {e}")

if "temp_prompt" in st.session_state and st.session_state["temp_prompt"]:
    user_prompt = st.session_state["temp_prompt"]
    st.session_state["temp_prompt"] = None

st.write("⌨️ **Step 2: Ya yahan likh ke bhejo**")
p = st.chat_input("Yahan likho... Garo / Khasi / Kokborok - Sab Roman me!")
if p:
    user_prompt = p

def get_ai_response(prompt_text, system_prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash"]
    for model_name in models_to_try:
        try:
            r = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                )
            )
            if r.text: return r.text
        except:
            time.sleep(1)
            continue
    return "Mitela! Server busy hai, 1 min baad try kar!"

if user_prompt:
    st.session_state.messages.append({"role":"user","content":user_prompt})
    st.chat_message("user").write(user_prompt)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... 🗣️")
        SYSTEM_PROMPT = f"""You are Megh-AI, created by Syrti-megh from Meghalaya. You know 5 languages: Garo, Khasi, Kokborok, Hindi, English.
        CRITICAL RULES:
        1. ALWAYS reply in ROMAN ENGLISH ONLY. Only A-Z letters. NEVER Devanagari.
        2. Hindi in Roman: 'Namaste kaise ho' NOT 'नमस्ते'.
        3. Reply language is {lang} but script ALWAYS Roman.
        4. Say I am Megh-AI created by Syrti-megh. Never say Gemini/Google.
        Keep short and clear for voice."""
        ans = get_ai_response(user_prompt, SYSTEM_PROMPT)
        box.markdown(ans)
        
        # AI BOLEGA - YAHAN VOICE AYEGA
        try:
            vname = VOICE_MAN.get(lang, "en-US-GuyNeural")
            voice_file = asyncio.run(make_voice(ans, vname, lang))
            if voice_file and os.path.exists(voice_file):
                st.success("🔊 AI bol raha hai...")
                st.audio(voice_file, autoplay=True)
            else:
                st.warning("Voice file nahi bana")
        except Exception as e:
            st.error(f"Voice Error: {e}")
            
    st.session_state.messages.append({"role":"assistant","content":ans})
    st.rerun()
