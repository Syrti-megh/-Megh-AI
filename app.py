import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time

st.set_page_config(page_title="Megh-AI", page_icon=":cloud:")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

st.title("Megh-AI")
st.caption("Meghalaya's FIRST Garo + Khasi AI | Better than Lemka")

VOICE_MAN = {
"English": "en-IN-PrabhatNeural", "Hindi": "hi-IN-MadhurNeural",
"Khasi": "en-IN-PrabhatNeural", "Garo": "en-IN-PrabhatNeural",
"Assamese": "bn-IN-BashkarNeural", "Auto": "en-IN-PrabhatNeural"
}

async def make_voice(text, vname, lang):
    if os.path.exists("voice.mp3"): os.remove("voice.mp3")
    import edge_tts
    clean_text = text.replace("*", "")[:500]
    rate = "-35%" if lang in ["Khasi","Garo"] else "-10%"
    communicate = edge_tts.Communicate(clean_text, vname, rate=rate)
    await communicate.save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state:
    st.session_state.messages = []
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("Language:", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything in Garo or Khasi...")

def get_ai_response(prompt_text, system_prompt):
    # Sahi order: 3.8 Flash -> 3.5 Flash-lite -> 3.8 Flash (retry)
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
            # 503 hai toh 2 sec ruk ke retry
            if "503" in str(e) or "high demand" in str(e).lower():
                time.sleep(2 * (attempt + 1))
                continue
            time.sleep(1)
            continue
    return "Mitela! Google ka 3.8 server abhi full busy hai. 1 min ruk ke fir se Hii likh de! / Khublei! 503 high demand hai."

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
            vname = VOICE_MAN.get(lang, "en-IN-PrabhatNeural")
            f = asyncio.run(make_voice(ans, vname, lang))
            st.audio(f, autoplay=True)
        except: pass
    st.session_state.messages.append({"role":"assistant","content":ans})
