import streamlit as st, subprocess, tempfile

def load_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    text = ""
    if ext == 'pdf':
        import fitz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
        doc = fitz.open(tmp.name)
        text = "\n".join(page.get_text() for page in doc)
        if not text.strip():
            text = perform_ocr(tmp.name)
    elif ext == 'txt':
        text = uploaded_file.read().decode('utf-8')
    elif ext == 'docx':
        import docx
        doc = docx.Document(uploaded_file)
        text = "\n".join(p.text for p in doc.paragraphs)
    else:
        text = "Unsupported file type"
    return text

def perform_ocr(pdf_path):
    from pdf2image import convert_from_path
    import pytesseract
    pages = convert_from_path(pdf_path)
    text = ""
    for i, page in enumerate(pages):
        st.info(f"OCR processing page {i+1}/{len(pages)}")
        text += pytesseract.image_to_string(page)
    return text

def summarize(text):
    prompt = f"Summarize this text:\n{text[:1000]}"
    try:
        result = subprocess.run(["ollama", "run", "mistral", prompt], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        return f"AI failed: {e}"

def generate_flashcards(summary):
    cards = []
    for s in summary.split('.'):
        s = s.strip()
        if len(s) > 20:
            cards.append({
                "question": f"What about: {s[:30]}...?",
                "answer": s
            })
    return cards[:10]

def export_to_apkg(cards, file_path):
    import genanki
    model = genanki.Model(
        1607392319, 'AnkiGamifyModel',
        fields=[{'name':'Question'},{'name':'Answer'}],
        templates=[{
            'name': 'Card',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr>{{Answer}}'
        }]
    )
    deck = genanki.Deck(2059400110, 'AnkiGamifyDeck')
    for c in cards:
        note = genanki.Note(model=model, fields=[c['question'], c['answer']])
        deck.add_note(note)
    genanki.Package(deck).write_to_file(file_path)

st.title("🃏 AnkiGamify")

uploaded_file = st.file_uploader("Upload PDF, TXT, or DOCX", type=['pdf','txt','docx'])

if uploaded_file:
    text = load_file(uploaded_file)
    st.text_area("Extracted Text", text[:1000]+"..." if len(text)>1000 else text, height=200)

    if st.button("Generate Flashcards"):
        summary = summarize(text)
        st.subheader("Summary")
        st.write(summary)

        cards = generate_flashcards(summary)
        st.subheader("Flashcards")
        for i, c in enumerate(cards, 1):
            st.markdown(f"**{i}. Q:** {c['question']}  \n**A:** {c['answer']}")

        if st.button("Export to Anki (.apkg)"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".apkg") as tmp:
                export_to_apkg(cards, tmp.name)
                st.download_button("Download Anki Deck", open(tmp.name, "rb").read(), "ankigamify_deck.apkg")
