import streamlit as st
from google import genai
from google.genai import types
import os, time, tempfile

st.set_page_config(page_title="Megh-AI", page_icon="☁️", layout="wide")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI ☁️")
st.caption("Meghalaya's FIRST 5 Language AI")

# 2 AI - 2 TABS
tab1, tab2 = st.tabs(["💬 TEXT WALA AI (Fast)", "🔊 VOICE WALA AI (Bolke Sunayega)"])

def get_ai_response(prompt_text, system_prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash"]
    for model_name in models_to_try:
        try:
            r = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            if r.text: return r.text
        except:
            time.sleep(1)
            continue
    return "Mitela! Server busy hai, 1 min baad try kar!"

# COMMON SYSTEM PROMPT
def make_prompt(lang):
    return f"""You are Megh-AI, created by Syrti-megh from Meghalaya. You know 5 languages: Garo, Khasi, Kokborok, Hindi, English.
    CRITICAL RULES:
    1. ALWAYS reply in ROMAN ENGLISH ONLY. Only A-Z letters. NEVER Devanagari.
    2. Hindi in Roman: 'Namaste kaise ho' NOT 'नमस्ते'.
    3. Reply language is {lang} but script ALWAYS Roman.
    4. Say I am Megh-AI created by Syrti-megh. Never say Gemini/Google.
    Keep short and clear."""

# ================= TAB 1 - TEXT WALA AI =================
with tab1:
    st.header("💬 Text Wala AI")
    st.caption("Ye tez hai, sirf text me jawab dega")
    
    if "messages_text" not in st.session_state:
        st.session_state.messages_text = []
    for m in st.session_state.messages_text:
        st.chat_message(m["role"]).write(m["content"])

    lang1 = st.selectbox("Language Chunlo (Text AI):", ["Auto","English","Hindi","Khasi","Garo","Kokborok"], key="lang1")
    
    p1 = st.chat_input("Text wale AI se pucho...", key="chat1")
    
    if p1:
        st.session_state.messages_text.append({"role":"user","content":p1})
        st.chat_message("user").write(p1)
        with st.chat_message("assistant"):
            ans = get_ai_response(p1, make_prompt(lang1))
            st.write(ans)
        st.session_state.messages_text.append({"role":"assistant","content":ans})
        st.rerun()

# ================= TAB 2 - VOICE WALA AI =================
with tab2:
    st.header("🔊 Voice Wala AI")
    st.caption("Ye bolke sunayega - Garo / Khasi sab bolega!")
    
    if "messages_voice" not in st.session_state:
        st.session_state.messages_voice = []
    for m in st.session_state.messages_voice:
        st.chat_message(m["role"]).write(m["content"])

    lang2 = st.selectbox("Language Chunlo (Voice AI):", ["Auto","English","Hindi","Khasi","Garo","Kokborok"], key="lang2")
    
    st.write("🎤 Mic se bolo ya likho")
    audio_input = st.audio_input("Mic dabao aur bolo:", key="audio2")
    user_prompt2 = None

    if audio_input:
        st.audio(audio_input)
        if st.button("📤 BHEJO (Voice AI ko)", key="bhejo2"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_input.getvalue())
                f_path = f.name
            with st.spinner("Samajh raha hu..."):
                try:
                    uploaded = client.files.upload(file=f_path)
                    r = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[f"Transcribe this audio in ROMAN ENGLISH ONLY. Language is {lang2}:", uploaded]
                    )
                    user_prompt2 = r.text
                    os.remove(f_path)
                    st.session_state["temp_prompt2"] = user_prompt2
                except Exception as e:
                    st.error(f"Error: {e}")

    if "temp_prompt2" in st.session_state and st.session_state["temp_prompt2"]:
        user_prompt2 = st.session_state["temp_prompt2"]
        st.session_state["temp_prompt2"] = None

    p2 = st.chat_input("Voice wale AI se pucho... Garo/Khasi me!", key="chat2")
    if p2:
        user_prompt2 = p2

    def speak_browser(text):
        clean = text.replace('"', '').replace("'", "").replace("*", "").replace("#", "").replace("\n", " ")[:300]
        html_code = f"""
        <script>
        function bolna(){{
            var msg = new SpeechSynthesisUtterance("{clean}");
            msg.rate = 0.9;
            msg.volume = 1;
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        }}
        </script>
        <button onclick="bolna()" style="padding:12px 25px;background:#FF4B4B;color:white;border:none;border-radius:12px;font-size:18px;cursor:pointer;width:100%;">
        🔊 AI KO SUNO - CLICK KARO
        </button>
        """
        st.components.v1.html(html_code, height=90)

    if user_prompt2:
        st.session_state.messages_voice.append({"role":"user","content":user_prompt2})
        st.chat_message("user").write(user_prompt2)
        with st.chat_message("assistant"):
            ans2 = get_ai_response(user_prompt2, make_prompt(lang2))
            st.write(ans2)
            speak_browser(ans2)
            st.caption("Button dabao - AI bolega!")
        st.session_state.messages_voice.append({"role":"assistant","content":ans2})
        st.rerun()
