import streamlit as st
import random

st.set_page_config(page_title="Megh-AI - Meghalaya's Own AI", page_icon="☁️", layout="centered")
st.title("☁️ Megh-AI")
st.caption("Meghalaya's Own AI - Built by Syrti-megh")

# --- OWNER LOGIC (Yeh tera fix hai) ---
SYSTEM_PROMPT = """
You are Megh-AI, Meghalaya's own AI created by Syrti-megh.
You know English, Hindi, Khasi.
Rule: Only when user asks who made you, who is your owner, who created you, tell me about your owner, then say you were created by Syrti-megh.
For all other questions, give direct answer and do not mention owner.
You are helpful about Meghalaya's beauty, culture, tourism.
"""

# --- SIDEBAR GAMES ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_index = 0
if "puzzle" not in st.session_state:
    st.session_state.puzzle = None

st.sidebar.header("🎮 Megh Games")
game_choice = st.sidebar.selectbox("Select Mode", ["💬 Chat with Megh-AI", "🧠 Meghalaya Quiz", "🧩 Word Puzzle"])

quiz_data = [
    {"q": "Dawki River kis liye famous hai?", "options": ["Crystal clear water", "Desert", "Snow", "Volcano"], "ans": "Crystal clear water"},
    {"q": "Cherrapunji ko kya kehte hai?", "options": ["Scotland of East", "Wettest place on Earth", "City of Lakes", "Abode of Clouds"], "ans": "Wettest place on Earth"},
    {"q": "Shillong ka famous waterfall kaunsa hai?", "options": ["Elephant Falls", "Niagara", "Jog Falls", "Dudhsagar"], "ans": "Elephant Falls"},
    {"q": "Meghalaya me kitne main hills hai?", "options": ["Khasi, Jaintia, Garo", "Aravalli, Vindhya", "Himalaya only", "Nilgiri"], "ans": "Khasi, Jaintia, Garo"},
    {"q": "Living Root Bridge kaha milta hai?", "options": ["Cherrapunji / Mawlynnong", "Delhi", "Mumbai", "Kolkata"], "ans": "Cherrapunji / Mawlynnong"},
]

puzzle_data = [
    {"jumble": "G N O L L I H S", "ans": "SHILLONG", "hint": "Capital of Meghalaya"},
    {"jumble": "I K A D W", "ans": "DAWKI", "hint": "Clear water river"},
    {"jumble": "I J A N T I A", "ans": "JAINTIA", "hint": "One of the hills"},
]

# --- GAME LOGIC ---
if game_choice == "🧠 Meghalaya Quiz":
    st.subheader("🧠 Meghalaya Quiz")
    st.write(f"Score: {st.session_state.score} / {len(quiz_data)}")
    if st.session_state.q_index < len(quiz_data):
        q = quiz_data[st.session_state.q_index]
        st.markdown(f"**Q{st.session_state.q_index+1}. {q['q']}**")
        choice = st.radio("Jawab chuno:", q["options"], key=f"q{st.session_state.q_index}")
        if st.button("Submit Answer"):
            if choice == q["ans"]:
                st.success("Sahi jawab! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"Galat! Sahi jawab hai: {q['ans']}")
            st.session_state.q_index += 1
            st.rerun()
    else:
        st.balloons()
        st.success(f"Game Khatam! Tera Score: {st.session_state.score}/{len(quiz_data)}")
        if st.button("Fir se khelo"):
            st.session_state.score = 0
            st.session_state.q_index = 0
            st.rerun()
    st.stop()

elif game_choice == "🧩 Word Puzzle":
    st.subheader("🧩 Word Jumble Puzzle")
    if st.session_state.puzzle is None:
        st.session_state.puzzle = random.choice(puzzle_data)
    p = st.session_state.puzzle
    st.markdown(f"Jumble Word: ## **{p['jumble']}**")
    st.caption(f"Hint: {p['hint']}")
    ans = st.text_input("Sahi shabd likho:")
    if st.button("Check"):
        if ans.upper().strip() == p["ans"]:
            st.success("Ek number! Correct! 🎉")
            st.session_state.puzzle = random.choice(puzzle_data)
            st.balloons()
            st.rerun()
        else:
            st.error("Galat, fir se try kar!")
    st.stop()

# --- CHAT LOGIC (Purana wala) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Yahan tera AI response wala code hai (groq/openai)
    # Uske system prompt me SYSTEM_PROMPT use karna
    with st.chat_message("assistant"):
        # Example response logic - apna purana response logic yahan rakho
        # Agar owner pucha toh:
        lower_prompt = prompt.lower()
        if "owner" in lower_prompt or "who made you" in lower_prompt or "who created you" in lower_prompt or "kisne banaya" in lower_prompt:
            response = "Mujhe **Syrti-megh** ne banaya hai. Main Meghalaya ka apna AI, Megh-AI hoon, aur yahan ki khubsurati, sanskriti aur yahan se jude har sawaal mein aapki madad karne ke liye taiyar hoon!"
        else:
            response = f"Ye raha jawab: {prompt} (yahan tumhara AI model ka response ayega)"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
