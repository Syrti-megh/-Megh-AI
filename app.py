import streamlit as st
from google import genai
from google.genai import types
import asyncio, os, time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

# Key safely nikalo + 2 key ka support
def get_keys():
    keys = []
    for k in ["GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]:
        if k in st.secrets:
            keys.append(st.secrets[k].strip().strip('"').strip("'"))
    return keys

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | English • हिंदी • Khasi • Garo • Assamese")

VOICE_MAN = {"English":"en-IN-PrabhatNeural","Hindi":"hi-IN-MadhurNeural","Khasi":"en-IN-PrabhatNeural","Garo":"en-IN-PrabhatNeural","Assamese":"bn-IN-BashkarNeural","Auto":"en-IN-PrabhatNeural"}

async def make_voice(text, vname):
    if os.path.exists("voice.mp3"): os.remove("voice.mp3")
    import edge_tts
    await edge_tts.Communicate(text.replace("*","")[:500], vname).save("voice.mp3")
    return "voice.mp3"

if "messages" not in st.session_state: st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

lang = st.selectbox("🗣️ Language:", ["Auto","English","Hindi","Khasi","Garo","Assamese"])
p = st.chat_input("Ask anything...")

if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... ⏳")
        SYSTEM = f"You are Megh-AI by Syrti-megh. Never say Gemini. Reply in {lang} if not Auto else same as user. Know English, Hindi, Khasi, Garo, Assamese."

        ans = None
        MODELS = ["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-2.0-flash"]
        KEYS = get_keys()

        for api_key in KEYS:
            client = genai.Client(api_key=api_key)
            for model_name in MODELS:
                try:
                    r = client.models.generate_content(
                        model=model_name,
                        contents=p,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM)
                    )
                    ans = r.text
                    break
                except Exception as e:
                    err = str(e)
                    if "429" in err or "503" in err:
                        time.sleep(1)
                        continue
                    else:
                        ans = f"Error: {err[:300]}"
                        break
            if ans: break

        if not ans:
            ans = "🙏 Server busy
