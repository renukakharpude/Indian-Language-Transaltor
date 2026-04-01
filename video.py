import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

st.title("🎬 Indian Language Video Translator")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv"])

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

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.video("temp_video.mp4")

    if st.button("Translate Video"):

        st.info("Loading Whisper model...")
        model = whisper.load_model("base")

        st.info("Extracting audio...")
        video = VideoFileClip("temp_video.mp4")
        audio_path = "audio.wav"
        video.audio.write_audiofile(audio_path)

        st.info("Transcribing audio...")
        result = model.transcribe(audio_path)
        original_text = result["text"]

        st.subheader("Original Text")
        st.write(original_text)

        st.info("Translating...")
        target_lang_code = language_options[selected_language]
        translated_text = GoogleTranslator(source="auto", target=target_lang_code).translate(original_text)

        st.subheader("Translated Text")
        st.write(translated_text)

        st.info("Generating translated audio...")
        tts = gTTS(translated_text, lang=target_lang_code)
        translated_audio_path = "translated_audio.mp3"
        tts.save(translated_audio_path)

        st.subheader("Translated Audio")
        st.audio(translated_audio_path)

        st.download_button(
            label="Download Translated Audio",
            data=open(translated_audio_path, "rb"),
            file_name="translated_audio.mp3",
            mime="audio/mp3"
        )

        # Cleanup
        os.remove(audio_path)
