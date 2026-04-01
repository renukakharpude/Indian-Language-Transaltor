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
    try:
        import speech_recognition as sr
    except:
        st.error("❌ Voice feature not supported in deployed app (use local system)")
        st.stop()

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
    try:
        import pytesseract
        from PIL import Image
    except:
        st.error("❌ OCR not supported in deployed app (use local system)")
        st.stop()

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
elif module == "🎬 Video":
    try:
        import whisper
        from moviepy.editor import VideoFileClip
        import yt_dlp
    except:
        st.error("❌ Video feature not supported in deployed app")
        st.stop()

    from deep_translator import GoogleTranslator
    from gtts import gTTS
    import os

    st.title("🎬 Video Translator")

    option = st.radio("Choose Input Type", ["Upload Video", "YouTube Link"])

    language_options = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
        "Kannada": "kn", "Malayalam": "ml",
        "Bengali": "bn", "Gujarati": "gu", "Marathi": "mr"
    }

    selected_language = st.selectbox("Select Language", list(language_options.keys()))
    video_path = None

    if option == "Upload Video":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
        if uploaded_file:
            video_path = "video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())
            st.video(video_path)

    else:
        youtube_url = st.text_input("Enter YouTube URL")
        if youtube_url:
            try:
                video_path = "yt.mp4"
                with yt_dlp.YoutubeDL({'outtmpl': video_path}) as ydl:
                    ydl.download([youtube_url])
                st.video(video_path)
            except Exception as e:
                st.error(e)

    if video_path and st.button("Translate Video"):
        try:
            model = whisper.load_model("base")
            video = VideoFileClip(video_path)
            audio_path = "audio.wav"
            video.audio.write_audiofile(audio_path)

            result = model.transcribe(audio_path)
            text = result["text"]

            st.write(text)

            translated = GoogleTranslator(source="auto", target=language_options[selected_language]).translate(text)
            st.write(translated)

            tts = gTTS(translated, lang=language_options[selected_language])
            tts.save("audio.mp3")
            st.audio("audio.mp3")

            os.remove(audio_path)

        except Exception as e:
            st.error(e)

# ---------------- PDF ---------------- #
elif module == "📄 PDF":
    try:
        import fitz
    except:
        st.error("❌ PDF feature not supported")
        st.stop()

    from gtts import gTTS
    from deep_translator import GoogleTranslator

    st.title("📄 PDF Translator")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    lang = st.selectbox("Select Language", list(languages.keys()))

    if uploaded_file and st.button("Convert"):
        try:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()

            st.text_area("Text", text)

            translated = GoogleTranslator(source="auto", target=languages[lang]).translate(text)
            st.text_area("Translated", translated)

            tts = gTTS(translated, lang=languages[lang])
            tts.save("pdf.mp3")
            st.audio("pdf.mp3")

        except Exception as e:
            st.error(e)
       


           
   

   

   
          

  


           

      
       

        
   
      

       

           
                    
   

    
    
            

   
  


     
  
                

            
       
