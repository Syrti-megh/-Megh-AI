import streamlit as st
from google import genai
from google.genai import types
import os, asyncio

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = "Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho. Banaya Syrti-megh ne. Tum Megh-AI ho, Gemini mat bolna."

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

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
        try:
            import edge_tts
            async def voice(t):
                if os.path.exists("v.mp3"): os.remove("v.mp3")
                c = edge_tts.Communicate(t[:400], "hi-IN-MadhurNeural")
                await c.save("v.mp3")
                return "v.mp3"
            f = asyncio.run(voice(ans))
            st.audio(f, autoplay=True)
        except:
            pass
    st.session_state.messages.append({"role":"assistant","content":ans})
