import streamlit as st
import fitz
import easyocr
from PIL import Image
import numpy as np

def extract_pdf(upload):
    doc = fitz.open(stream=upload.read(), filetype="pdf")
    return "\n".join([p.get_text() for p in doc])

def extract_image(upload):
    image = Image.open(upload)
    result = easyocr.Reader(['en'], gpu=False).readtext(np.array(image), detail=0)
    return "\n".join(result)

def load_input_source():
    source = st.selectbox("Select Input Source", ["Manual", "PDF", "Image (OCR)", "Text"])
    upload = None
    if source != "Manual":
        upload = st.file_uploader("Upload File")

    if source == "Manual":
        return source, st.text_area("Enter text")
    elif upload:
        if source == "PDF":
            return source, extract_pdf(upload)
        elif source == "Image (OCR)":
            return source, extract_image(upload)
        elif source == "Text":
            return source, upload.read().decode("utf-8")
    return source, ""
