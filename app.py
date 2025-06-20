import streamlit as st
from utils.extract import load_input_source
from utils.summarizer import summarize
from utils.flashcards import generate_cards
from utils.exporter import download_csv, download_apkg
from ui.layout import show_header, show_preview, show_exports

st.set_page_config(page_title="AnkiGamify", layout="wide")
show_header()

source, raw_text = load_input_source()

if raw_text:
    show_preview("📄 Extracted/Input Text", raw_text)

    if st.button("🧪 Summarize & Generate Cards"):
        summary = summarize(raw_text)
        st.success("Summary generated.")
        st.markdown(f"**🔍 Summary:** {summary}")
        cards = generate_cards(summary)
        st.markdown("### 📇 Flashcards Preview")
        for i, c in enumerate(cards):
            st.markdown(f"**{i+1}.** Q: {c['question']}<br>A: {c['answer']}", unsafe_allow_html=True)
        show_exports(cards)
