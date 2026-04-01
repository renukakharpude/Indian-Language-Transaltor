import streamlit as st
import base64

# ---------------- BACKGROUND FUNCTION ---------------- #
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .block-container {{
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 15px;
    }}

    html, body, [class*="css"] {{
        color: black !important;
    }}

    h1, h2, h3, h4, h5, h6, p, label, span, div {{
        color: black !important;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# ---------------- UI CONFIG ---------------- #
st.set_page_config(page_title="AI Language Translator", layout="wide")

# 👉 SET BACKGROUND IMAGE
set_bg("image.png")

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🌍 Language Translator")
module = st.sidebar.radio(
    "Select Module",
    ["🏠 Home", "🎤 Voice", "🖼 Image", "🎬 Video", "📄 PDF"]
)

# ---------------- LANGUAGES ---------------- #
languages = {
    "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu",
    "Punjabi": "pa", "Bengali": "bn", "Assamese": "as",
    "Odia": "or", "Tamil": "ta", "Telugu": "te",
    "Kannada": "kn", "Malayalam": "ml", "Urdu": "ur",
    "Sanskrit": "sa", "Konkani": "gom", "Manipuri": "mni",
    "Bodo": "brx", "Dogri": "doi", "Maithili": "mai",
    "Santali": "sat", "Sindhi": "sd", "Kashmiri": "ks",
    "Nepali": "ne", "English": "en"
}

# ---------------- HOME ---------------- #
if module == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🌍 Indian Language Translator</h1>", unsafe_allow_html=True)

    st.markdown("""
    ### 🚀 Features
    - 🎤 Real-Time Voice Translation  
    - 🖼 Image OCR Translation  
    - 🎬 Video Translation  
    - 📄 PDF to Speech  

    ---
    ### 🧠 Technologies
    - Whisper (AI Speech Recognition)
    - Tesseract OCR
    - Google Translator
    - gTTS (Speech Output)
    """)

# ---------------- VOICE ---------------- #
elif module == "🎤 Voice":
    import speech_recognition as sr
    from deep_translator import GoogleTranslator
    from gtts import gTTS

    st.title("🎤 Real-Time Voice Translator")

    lang = st.selectbox("Select Language", list(languages.keys()))

    if st.button("Start Recording"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Speak now...")
                audio = r.listen(source)

            text = r.recognize_google(audio)
            st.success(text)

            translated = GoogleTranslator(source="auto", target=languages[lang]).translate(text)
            st.success(translated)

            tts = gTTS(translated, lang=languages[lang])
            tts.save("voice.mp3")
            st.audio("voice.mp3")

        except Exception as e:
            st.error(e)

# ---------------- IMAGE ---------------- #
elif module == "🖼 Image":
    import pytesseract
    from PIL import Image
    from deep_translator import GoogleTranslator
    import platform

    st.title("🖼 Image Translator")

    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    file = st.file_uploader("Upload Image", type=["jpg", "png"])
    lang = st.selectbox("Select Language", list(languages.keys()))

    if file:
        try:
            img = Image.open(file)
            st.image(img)

            text = pytesseract.image_to_string(img)
            st.write(text)

            translated = GoogleTranslator(source="auto", target=languages[lang]).translate(text)
            st.success(translated)

        except Exception as e:
            st.error(e)

# ---------------- VIDEO (UPDATED FAST VERSION) ---------------- #
elif module == "🎬 Video":
    from faster_whisper import WhisperModel
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    import yt_dlp
    import os
    import glob
    from moviepy.editor import AudioFileClip

    st.title("⚡ Fast YouTube Video Translator")

    language_options = {
        "Hindi": "hi",
        "Marathi": "mr",
        "Tamil": "ta",
        "Telugu": "te"
    }

    selected_language = st.selectbox("Select Language", list(language_options.keys()))
    youtube_url = st.text_input("📺 Paste YouTube URL")

    if st.button("🚀 Translate Video"):

        if not youtube_url:
            st.error("❌ Please enter YouTube URL")
            st.stop()

        for f in glob.glob("audio*"):
            os.remove(f)

        st.info("⬇️ Downloading audio...")

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        audio_file = [f for f in os.listdir() if f.startswith("audio")][0]

        st.info("✂️ Trimming audio...")

        clip = AudioFileClip(audio_file)
        short_clip = clip.subclip(0, min(120, clip.duration))
        short_clip.write_audiofile("short_audio.wav", verbose=False, logger=None)

        st.info("🧠 Transcribing...")

        model = WhisperModel("tiny", compute_type="int8")
        segments, _ = model.transcribe("short_audio.wav", beam_size=1)
        text = " ".join([seg.text for seg in segments])

        st.subheader("📝 Original Text")
        st.write(text)

        st.info("🌍 Translating...")

        target_lang = language_options[selected_language]

        try:
            translated_text = GoogleTranslator(source="auto", target=target_lang).translate(text)
        except:
            translated_text = text

        st.subheader("🔤 Translated Text")
        st.write(translated_text)

        st.info("🔊 Generating voice...")

        tts = gTTS(translated_text, lang=target_lang)
        tts.save("output.mp3")

        st.audio("output.mp3")

        with open("output.mp3", "rb") as f:
            st.download_button("⬇️ Download Audio", f, "translated_audio.mp3")

        st.success("⚡ Done (Fast Mode)")

# ---------------- PDF ---------------- #
elif module == "📄 PDF":
    import fitz
    from gtts import gTTS
    from PIL import Image
    import pytesseract
    import platform
    from deep_translator import GoogleTranslator

    st.title("📄 PDF → Translate → Speech")

    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    lang = st.selectbox("Select Language", list(languages.keys()))
    lang_code = languages[lang]

    page_input = st.text_input("Page Number / Range (e.g. 1 or 2-5)", "1")

    def get_pages(value):
        try:
            if "-" in value:
                start, end = map(int, value.split("-"))
                return list(range(start - 1, end))
            else:
                return [int(value) - 1]
        except:
            return None

    if uploaded_file is not None and st.button("🚀 Convert"):

        pages = get_pages(page_input)
        if pages is None:
            st.error("Invalid page input")
            st.stop()

        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        extracted_text = []

        for i in pages:
            if i < 0 or i >= len(doc):
                continue

            page = doc.load_page(i)
            text = page.get_text()

            if not text.strip():
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)

            extracted_text.append(text)

        final_text = " ".join(extracted_text).strip()

        st.text_area("Extracted Text", final_text, height=200)

        translated_text = GoogleTranslator(source="auto", target=lang_code).translate(final_text)

        st.text_area("Translated Text", translated_text, height=200)

        tts = gTTS(translated_text, lang=lang_code)
        tts.save("pdf_audio.mp3")

        st.audio("pdf_audio.mp3")
        st.success("✅ Done!")
