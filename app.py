import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time

st.set_page_config(page_title="Megh-AI", page_icon=":cloud:")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's FIRST Garo + Khasi AI | Better than Lemka")

# UPDATED - VOCAL CLEAR MAN VOICE
VOICE_MAN = {
"English": "en-US-GuyNeural",
"Hindi": "hi-IN-MadhurNeural",
"Khasi": "en-US-GuyNeural",
"Garo": "en-US-GuyNeural",
"Assamese": "bn-IN-BashkarNeural",
"Auto": "en-US-GuyNeural"
}

async def make_voice(text, vname, lang):
    if os.path.exists("voice.mp3"): 
        os.remove("voice.mp3")
    import edge_tts
    # Clear ke liye special chars hatao
    clean_text = text.replace("*", "").replace("'", " ").replace("!", ".").replace("#", "")[:400]
    
    if lang in ["Khasi", "Garo"]:
        # Khasi ke liye SLOW + CLEAR + VOCAL MAN
        vname = "en-US-GuyNeural"
        rate = "-25%"  # slow
        volume = "+25%"  # vocal loud
        pitch = "+4Hz"   # thoda vocal
        # Khasi words ko clear bolne ke liye
        clean_text = clean_text.replace("Khublei", "Khoob Lay")
        clean_text = clean_text.replace("Nga dei", "Nga Day")
        clean_text = clean_text.replace("Syrti-megh", "Sirti Megh")
        clean_text = clean_text.replace("Meghalaya", "Mayghalaya")
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

lang = st.selectbox("Language:", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything in Garo or Khasi...")

def get_ai_response(prompt_text, system_prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash"]
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
            if "503" in str(e) or "high demand" in str(e).lower():
                time.sleep(2 * (attempt + 1))
                continue
            time.sleep(1)
            continue
    return "Mitela! Google ka 3.8 server abhi full busy hai. 1 min ruk ke fir se Hii likh de! / Khublei!"

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu...")
        SYSTEM_PROMPT = f"You are Megh-AI, created by Syrti-megh from Meghalaya. You know Garo + Khasi. If asked who made you, say I am Megh-AI created by Syrti-megh. Never say Gemini or Google. Garo: Nameng=Hello. Khasi: Khublei. Reply in {lang}."
        ans = get_ai_response(p, SYSTEM_PROMPT)
        box.markdown(ans)
        try:
            vname = VOICE_MAN.get(lang, "en-US-GuyNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except: pass
    st.session_state.messages.append({"role":"assistant","content":ans})
