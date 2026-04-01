import streamlit as st
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator

# Set Tesseract Path (CHANGE if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.title("📷 Image OCR & Indian Language Translator")

# Full Language Names
languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

target_language = st.selectbox(
    "Select Target Language",
    list(languages.keys())
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    try:
        # OCR Extraction
        extracted_text = pytesseract.image_to_string(image, lang='eng')

        st.subheader("📝 Extracted Text")
        st.write(extracted_text)

        if extracted_text.strip() != "":
            # Translation
            translated_text = GoogleTranslator(
                source='auto',
                target=languages[target_language]
            ).translate(extracted_text)

            st.subheader(f"🌍 Translated to {target_language}")
            st.success(translated_text)
        else:
            st.warning("No text detected in image.")

    except Exception as e:
        st.error(f"Error: {e}")
