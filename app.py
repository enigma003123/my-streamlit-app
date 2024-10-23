













import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import os
from pydub import AudioSegment

# Title of the app
st.title("Audio to Text Translator")

# Language selection for audio (including Arabic)
audio_language = st.selectbox("Select the language of the audio", 
                                ["en", "fr", "es", "de", "it", "zh", "ja", "ru", "ar"])

# File uploader widget
uploaded_file = st.file_uploader("Upload a .wav audio file", type=["wav"])

if uploaded_file is not None:
    # Save the uploaded audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Convert audio to text
            text = recognizer.recognize_google(audio_data, language=audio_language)
            st.write("Transcribed Text:")
            st.write(text)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")

    # Language Selection for Translation
    target_language = st.selectbox("Select target language for translation", 
                                    ["fr", "de", "es", "it", "zh", "ja", "ru", "ar"])

    if st.button("Translate"):
        # Translate the text
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        st.write("Translated Text:")
        st.write(translated_text)

        # Convert translated text to audio
        tts = gTTS(translated_text, lang=target_language)
        
        # Save the audio file as mp3 first
        mp3_file_path = tempfile.mktemp(suffix=".mp3")
        tts.save(mp3_file_path)

        # Convert the mp3 file to wav format using pydub
        wav_file_path = tempfile.mktemp(suffix=".wav")
        audio_segment = AudioSegment.from_mp3(mp3_file_path)
        audio_segment.export(wav_file_path, format="wav")

        # Provide audio playback option
        st.audio(wav_file_path, format='audio/wav')

        # Add download button for the translated audio in wav format
        with open(wav_file_path, "rb") as audio_file:
            st.download_button(
                label="Download Translated Audio (WAV)",
                data=audio_file,
                file_name="translated_audio.wav",
                mime="audio/wav"
            )

        # Clean up temporary files
        if st.button("Delete Temporary Files"):
            os.remove(temp_file_path)
            os.remove(mp3_file_path)  # Remove the MP3 file if needed
            os.remove(wav_file_path)   # Remove the WAV file if needed
            st.success("Temporary files deleted.")

