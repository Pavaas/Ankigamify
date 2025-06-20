import streamlit as st
from utils.loader import load_input_file
from utils.flashcard_generator import generate_flashcards
from utils.exporter import export_to_apkg, export_to_csv
from components.sidebar import render_sidebar
from components.pdf_viewer import render_pdf_viewer
from components.theme_toggle import dark_light_theme_toggle
from components.pipeline_visualizer import show_pipeline_status

# --- Page Setup ---
st.set_page_config(
    page_title="AnkiGamify",
    page_icon="🧠",
    layout="wide",
)

# --- Theme Toggle ---
dark_light_theme_toggle()

# --- Sidebar ---
render_sidebar()

# --- Main Header ---
st.markdown("## 🧠 AnkiGamify: AI-Powered Flashcard Wizard")
st.markdown("Turn PDFs, YouTube, Audio, and Notes into Anki-Ready Cards")

# --- Input Upload ---
uploaded_file = st.file_uploader("📂 Upload your study material", type=["pdf", "txt", "docx", "epub", "mp3", "wav"])
if uploaded_file:
    with st.spinner("🧪 Processing file..."):
        text, page_map = load_input_file(uploaded_file)
        st.success("✅ File processed successfully!")

        # Optional PDF preview
        if uploaded_file.name.endswith(".pdf"):
            render_pdf_viewer(uploaded_file)

        # Pipeline status
        show_pipeline_status(stage="Peristalsis")

        # Generate Flashcards
        flashcards = generate_flashcards(text, page_map)

        if flashcards:
            st.success(f"✅ {len(flashcards)} flashcards generated!")
            st.write("---")
            for i, card in enumerate(flashcards, 1):
                st.markdown(f"### Card {i}")
                st.markdown(card["question"], unsafe_allow_html=True)
                if card["type"] == "memo":
                    st.info(f"📝 Memo Explanation: {card['answer']}")
                else:
                    st.markdown(f"**Answer:** {card['answer']}")

            # Export Options
            st.write("---")
            st.markdown("### 📤 Export Flashcards")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬇️ Export to .apkg"):
                    export_to_apkg(flashcards, deck_name="AnkiGamify_Deck")
                    st.success("Saved as Anki Deck!")
            with col2:
                if st.button("📁 Export to .csv"):
                    export_to_csv(flashcards)
                    st.success("Saved as CSV File!")

# Footer
st.markdown("---")
st.markdown("📬 Contact: [Instagram](https://www.instagram.com/dr.pavanreddy) | [Email](mailto:Pavanreddy337@gmail.com) | [GitHub](https://github.com/Pavaas)")
