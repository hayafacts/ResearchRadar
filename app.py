import streamlit as st

st.set_page_config(
    page_title="ResearchRadar",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 ResearchRadar")

st.write(
    "An AI-powered research assistant using live web and Google Scholar search data."
)

topic = st.text_input(
    "What would you like to research?",
    placeholder="Example: Impact of AI on education"
)

if st.button("Search"):
    if topic:
        st.success(f"Searching for: {topic}")
    else:
        st.warning("Please enter a research topic.")