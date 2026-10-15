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

# FIXED - SAHI MODELS JO EXIST KARTE HAI
def get_ai_response(prompt_text, system_prompt):
    models_to_try = [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-8b", 
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash"
    ]
    for model_name in models_to_try:
        try:
            r = client.models.generate_content(
                model=model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(system_instruction=system_prompt)
            )
            if r.text and "Quota exceeded" not in r.text: 
                return r.text
        except Exception as e:
            if "Quota exceeded" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            time.sleep(1)
            continue
    return "Bhai thoda ruk ja! API limit khatam. 1 min baad try kar. Naya API Key bana le aistudio.google.com se!"

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
    
    p1 = st.chat_input("Text wale AI se
