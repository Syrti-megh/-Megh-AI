import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

API_KEY = st.secrets["GEMINI_API_KEY"].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

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
        
        # --- 3.8 FLASH WITH AUTO-RETRY FOR 503 ---
        ans = ""
        for attempt in range(3):
            try:
                r = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=p,
                    config=types.GenerateContentConfig(
                        system_instruction="You are Megh-AI, Meghalaya's Own AI. You were made by Syrti-megh. Never say you are Gemini. Keep answer short and clear."
                    )
                )
                ans = r.text
                break
            except Exception as e:
                err = str(e)
                if "503" in err or "overloaded" in err.lower():
                    time.sleep(2) # 2 sec ruk ke fir try karega
                    continue
                else:
                    ans = f"Error: {err}"
                    break
        
        if not ans:
            ans = "Server thoda busy hai Meghalaya ka network slow hai, 2 sec me fir se bolo 🙏"
        
        box.markdown(ans)
    
    st.session_state.messages.append({"role":"assistant","content":ans})
