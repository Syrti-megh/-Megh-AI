import streamlit as st
from google import genai

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

# --- API KEY FIX ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    API_KEY = API_KEY.strip().strip('"').strip("'")
except:
    st.error("GEMINI_API_KEY Secrets me nahi mila!")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI 🇮🇳 | Made with ❤️ in Meghalaya")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Ask anything...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        try:
            # Sahi Model ka naam - Ye 3.8 jaisa hi latest hai
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"You are Megh-AI, Meghalaya's Own AI, made by Syrti-megh. Never say you are Gemini. User: {prompt}"
            )
            ans = response.text
            st.write(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            # Ab error hide nahi hoga, saaf dikhega
            st.error(f"Real Error: {e}")
            st.write(f"Real Error: {e}")
