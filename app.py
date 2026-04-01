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

    /* Light glass effect */
    .block-container {{
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 15px;
    }}

    /* 🔥 MAKE ALL TEXT BLACK */
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

# ---------------- VIDEO ---------------- #

     # ---------------- VIDEO ---------------- #
elif module == "🎬 Video":
    import whisper
    from moviepy.editor import VideoFileClip
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    import os
    import yt_dlp

    st.title("🎬 Video Translator (Upload + YouTube Link)")

    option = st.radio("Choose Input Type", ["Upload Video", "YouTube Link"])

    language_options = {
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Marathi": "mr"
    }

    selected_language = st.selectbox("Select Target Language", list(language_options.keys()))

    video_path = None

    # ---------------- UPLOAD VIDEO ---------------- #
    if option == "Upload Video":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv"])

        if uploaded_file is not None:
            video_path = "uploaded_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            st.video(video_path)

    # ---------------- YOUTUBE LINK ---------------- #
    else:
        youtube_url = st.text_input("Enter YouTube Video URL")

        if youtube_url:
            try:
                video_path = "youtube_video.mp4"

                ydl_opts = {
                    'outtmpl': video_path,
                    'format': 'mp4'
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])

                st.video(video_path)

            except Exception as e:
                st.error(f"Download Error: {e}")

    # ---------------- TRANSLATE ---------------- #
    if video_path and st.button("Translate Video"):

        try:
            st.info("🔄 Loading AI model...")
            model = whisper.load_model("base")

            st.info("🎧 Extracting audio...")
            video = VideoFileClip(video_path)
            audio_path = "audio.wav"
            video.audio.write_audiofile(audio_path)

            st.info("🧠 Transcribing...")
            result = model.transcribe(audio_path)
            original_text = result["text"]

            st.subheader("📝 Original Text")
            st.write(original_text)

            st.info("🌍 Translating...")
            target_lang_code = language_options[selected_language]
            translated_text = GoogleTranslator(source="auto", target=target_lang_code).translate(original_text)

            st.subheader("🔤 Translated Text")
            st.write(translated_text)

            st.info("🔊 Generating Audio...")
            tts = gTTS(translated_text, lang=target_lang_code)
            tts.save("translated_audio.mp3")

            st.audio("translated_audio.mp3")

            st.download_button(
                "⬇️ Download Audio",
                data=open("translated_audio.mp3", "rb"),
                file_name="translated_audio.mp3"
            )

            os.remove(audio_path)

        except Exception as e:
            st.error(e)

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
        st.info("📄 Extracting text...")

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

        if not final_text:
            st.warning("No text found")
            st.stop()

        st.subheader("📄 Extracted Text")
        st.text_area("", final_text, height=200)

        st.info("🌍 Translating...")

        def translate_chunks(text, lang):
            max_chars = 400
            parts = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            translated_parts = []

            for part in parts:
                try:
                    translated = GoogleTranslator(source="auto", target=lang).translate(part)
                except:
                    translated = part
                translated_parts.append(translated)

            return " ".join(translated_parts)

        translated_text = translate_chunks(final_text, lang_code)

        st.subheader("🔤 Translated Text")
        st.text_area("", translated_text, height=200)

        st.info("🔊 Generating audio...")

        def text_to_speech_chunks(text, lang):
            max_chars = 500
            parts = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            audio_files = []

            for i, part in enumerate(parts):
                filename = f"part_{i}.mp3"
                tts = gTTS(part, lang=lang)
                tts.save(filename)
                audio_files.append(filename)

            return audio_files

        audio_parts = text_to_speech_chunks(translated_text, lang_code)

        for audio in audio_parts:
            st.audio(audio)

        if audio_parts:
            with open(audio_parts[0], "rb") as f:
                st.download_button("⬇️ Download Audio", f, "translated_audio.mp3")

        st.success("✅ Translation + Speech Completed!")


   
  
   


        
   
      

       

           
                    
   

    
    
            

   
  


     
  
                

            
       
