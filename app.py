import streamlit as st
import os
from utils.loader import load_input_file
from utils.flashcard_generator import generate_flashcards
from utils.exporter import export_flashcards
from utils.ui import show_pdf_viewer, sidebar_pipeline, show_footer
from utils.memo_card import generate_memo_cards

st.set_page_config(page_title="AnkiGamify", layout="wide")

# --- Sidebar & Branding ---
sidebar_pipeline()

st.title("🧠 AnkiGamify - AI Flashcard Generator")
st.markdown("Create high-quality flashcards like AnKing/UWorld from PDFs, Docs, YouTube, and more.")

# --- File Upload Section ---
uploaded_file = st.file_uploader(
    "📤 Upload PDF, DOCX, EPUB, TXT, MP3, or paste a YouTube link",
    type=["pdf", "docx", "epub", "txt", "mp3"]
)

yt_link = st.text_input("Or paste a YouTube link:")

if uploaded_file or yt_link:
    with st.spinner("🔍 Processing input..."):
        raw_text, page_map = load_input_file(uploaded_file, yt_link)
        if not raw_text:
            st.error("Failed to process file/link.")
        else:
            st.success("✅ Content loaded successfully.")
            show_pdf_viewer(uploaded_file)

            # --- Flashcard Generation Section ---
            st.markdown("---")
            st.header("🧩 Flashcard Settings")
            card_type = st.selectbox("Choose card type", ["Basic", "Cloze", "Memo Card", "AnKing-style"])

            if st.button("🎯 Generate Flashcards"):
                with st.spinner("🧠 Thinking... Generating cards..."):
                    if card_type == "Memo Card":
                        cards = generate_memo_cards(raw_text, page_map)
                    else:
                        cards = generate_flashcards(raw_text, card_type)
                    
                    if cards:
                        st.success(f"✅ Generated {len(cards)} flashcards!")
                        export_flashcards(cards)
                    else:
                        st.warning("😕 No flashcards were generated.")

# --- Footer ---
show_footer()
