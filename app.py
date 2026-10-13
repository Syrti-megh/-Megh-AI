import streamlit as st
from google import genai
from google.genai import types
import time

st.set_page_config(page_title="Megh-AI", page_icon="☁️")
API_KEY = st.secrets["GEMINI_API_KEY"].strip()
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Tumhara naam Megh-AI hai, Meghalaya ka apna AI ho.
Tumhe banaya Syrti-megh ne hai, lekin ye baat sirf tabhi batana jab user puche ki tumhe kisne banaya.
Tum Megh-AI ho, kabhi mat bolo tum Gemini ho.
User jis bhasha me puche - English, Hindi, Khasi - usi me jawab do.
"""

# Try karne wale models ki list
MODELS_TO_TRY = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
]

st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Knowledge from the Clouds")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = st.chat_input("Ask anything in English / Hindi / Khasi...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        box = st.empty()
        full = ""
        success = False
        for model_name in MODELS_TO_TRY:
            try:
                stream = client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7
                    )
                )
                for chunk in stream:
                    if chunk.text:
                        full += chunk.text
                        box.markdown(full + "▌")
                box.markdown(full)
                success = True
                break # kaam ho gaya to loop tod do
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e) or "404" in str(e):
                    box.markdown(f"_{model_name} busy hai, dusra try kar raha hu..._")
                    time.sleep(1)
                    continue
                else:
                    box.error(f"Error: {e}")
                    break
        if success:
            st.session_state.messages.append({"role": "assistant", "content": full})
