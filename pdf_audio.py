import streamlit as st
from gtts import gTTS
from PIL import Image
import pytesseract
import fitz
import os
import platform
from deep_translator import GoogleTranslator

# ---------------------- Tesseract path ---------------------- #
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="PDF Translator + Speech", page_icon="📄🎤")
st.title("📄 PDF → Translate → Speech")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# ---------------------- Language ---------------------- #
language_dict = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te"
}

selected_lang = st.selectbox("Select Language", list(language_dict.keys()))
lang_code = language_dict[selected_lang]

# ---------------------- Page Input ---------------------- #
page_input = st.text_input("Page Number / Range (e.g. 1 or 2-5)", "1")

def get_pages(value):
    if "-" in value:
        start, end = map(int, value.split("-"))
        return list(range(start-1, end))
    else:
        return [int(value)-1]

# ---------------------- MAIN ---------------------- #
if uploaded_file and st.button("🚀 Convert"):

    try:
        pages = get_pages(page_input)
    except:
        st.error("Invalid page input")
        st.stop()

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    extracted_text = []
    st.info("📄 Extracting text...")

    for i in pages:
        page = doc.load_page(i)
        text = page.get_text()

        if not text.strip():
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)

        extracted_text.append(text)

    final_text = " ".join(extracted_text).strip()

    if not final_text:
        st.warning("No text found")
        st.stop()

    st.subheader("📄 Extracted Text")
    st.text_area("", final_text, height=200)

    # ---------------------- TRANSLATION (FIX) ---------------------- #
    st.info("🌍 Translating...")

    def translate_chunks(text, lang):
        max_chars = 400
        parts = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        translated_parts = []

        for part in parts:
            try:
                translated = GoogleTranslator(source="auto", target=lang).translate(part)
                translated_parts.append(translated)
            except:
                translated_parts.append(part)

        return " ".join(translated_parts)

    translated_text = translate_chunks(final_text, lang_code)

    st.subheader("🔤 Translated Text")
    st.text_area("", translated_text, height=200)

    # ---------------------- TTS ---------------------- #
    st.info("🔊 Generating audio...")

    def text_to_speech_chunks(text, lang):
        max_chars = 500
        parts = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        audio_files = []

        for i, part in enumerate(parts):
            tts = gTTS(part, lang=lang)
            filename = f"part_{i}.mp3"
            tts.save(filename)
            audio_files.append(filename)

        return audio_files

    audio_parts = text_to_speech_chunks(translated_text, lang_code)

    for audio in audio_parts:
        st.audio(audio)

    with open(audio_parts[0], "rb") as f:
        st.download_button("⬇️ Download Audio", f, "translated_audio.mp3")

    st.success("✅ Translation + Speech Completed!")