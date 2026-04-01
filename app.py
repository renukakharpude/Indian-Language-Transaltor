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
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# ---------------- UI CONFIG ---------------- #
st.set_page_config(page_title="AI Language Translator", layout="wide")

set_bg("image.png")

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🌍 Language Translator")

# ❌ Removed Voice (causes error in cloud)
module = st.sidebar.radio(
    "Select Module",
    ["🏠 Home", "🎬 Video", "📄 PDF"]
)

# ---------------- LANGUAGES ---------------- #
languages = {
    "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn",
    "Malayalam": "ml", "Bengali": "bn", "English": "en"
}

# ---------------- HOME ---------------- #
if module == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🌍 Indian Language Translator</h1>", unsafe_allow_html=True)

    st.warning("⚠️ Voice & Image OCR features are disabled in cloud. Run locally for full features.")

    st.markdown("""
    ### 🚀 Features
    - 🎬 Video Translation  
    - 📄 PDF to Speech  

    ---
    ### 🧠 Technologies
    - Whisper (AI Speech Recognition)
    - Google Translator
    - gTTS (Speech Output)
    """)

# ---------------- VIDEO ---------------- #
elif module == "🎬 Video":
    import whisper
    from moviepy.editor import VideoFileClip
    from deep_translator import GoogleTranslator
    from gtts import gTTS
    import os

    st.title("🎬 Video Translator")

    language_options = {
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Marathi": "mr"
    }

    selected_language = st.selectbox("Select Target Language", list(language_options.keys()))

    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

    if uploaded_file:
        video_path = "video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        st.video(video_path)

        if st.button("Translate Video"):
            try:
                st.info("🔄 Loading Model...")
                model = whisper.load_model("tiny")   # ✅ FIXED (light model)

                st.info("🎧 Extracting Audio...")
                video = VideoFileClip(video_path)
                audio_path = "audio.wav"
                video.audio.write_audiofile(audio_path)

                st.info("🧠 Transcribing...")
                result = model.transcribe(audio_path)
                text = result["text"]

                st.subheader("📝 Original Text")
                st.write(text)

                st.info("🌍 Translating...")
                translated = GoogleTranslator(
                    source="auto",
                    target=language_options[selected_language]
                ).translate(text)

                st.subheader("🔤 Translated Text")
                st.write(translated)

                st.info("🔊 Generating Audio...")
                tts = gTTS(translated, lang=language_options[selected_language])
                tts.save("output.mp3")

                st.audio("output.mp3")

                os.remove(audio_path)

            except Exception as e:
                st.error(e)

# ---------------- PDF ---------------- #
elif module == "📄 PDF":
    import fitz
    from gtts import gTTS
    from deep_translator import GoogleTranslator

    st.title("📄 PDF Translator")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    lang = st.selectbox("Select Language", list(languages.keys()))

    if uploaded_file and st.button("Translate PDF"):
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

            text = ""
            for page in doc:
                text += page.get_text()

            st.subheader("📄 Extracted Text")
            st.text_area("", text, height=200)

            translated = GoogleTranslator(
                source="auto",
                target=languages[lang]
            ).translate(text)

            st.subheader("🔤 Translated Text")
            st.text_area("", translated, height=200)

            tts = gTTS(translated, lang=languages[lang])
            tts.save("pdf_audio.mp3")

            st.audio("pdf_audio.mp3")

        except Exception as e:
            st.error(e)
   

    
    
            

   
  


     
  
                

            
       
