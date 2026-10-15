import streamlit as st
from google import genai
from google.genai import types
import os, asyncio
import edge_tts

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())

SYSTEM_PROMPT = "Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho. Banaya Syrti-megh ne. Tum Megh-AI ho, Gemini mat bolna."

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya")

voice = "hi-IN-MadhurNeural"
async def make_voice(text):
    if os.path.exists("v.mp3"): os.remove("v.mp3")
    comm = edge_tts.Communicate(text[:400], voice)
    await comm.save("v.mp3")
    return "v.mp3"
def speak(t):
    f = asyncio.run(make_voice(t))
    st.audio(f, autoplay=True)

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages: st.chat_message(m["role"]).write(m["content"])

p = st.chat_input("Ask anything...")
if p:
    st.session_state.messages.append({"role":"user","content":p})
    st.chat_message("user").write(p)
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown("Soch raha hu... ⏳")
        try:
            r = client.models.generate_content(model="gemini-3.8-flash", contents=p, config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
            ans = r.text
        except:
            r = client.models.generate_content(model="gemini-2.0-flash-lite", contents=p, config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT))
            ans = r.text
        box.markdown(ans)
        speak(ans)
    st.session_state.messages.append({"role":"assistant","content":ans})
