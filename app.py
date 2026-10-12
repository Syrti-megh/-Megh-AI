import streamlit as st

st.set_page_config(page_title="Megh-AI", page_icon="☁️")

st.title("☁️ Megh-AI")
st.subheader("Meghalaya ka apna AI - Baadalon se bhi tez")

user_input = st.text_input("Apna sawal puchho:")

if user_input:
    st.success(f"Tumne pucha: {user_input}")
    st.write("Megh-AI soch raha hai... (Jald hi isme real AI jodega!)")
    st.balloons()

st.sidebar.markdown("Made with ❤️ in Meghalaya by Syrti-megh")
