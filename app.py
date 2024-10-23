# from deep_translator import GoogleTranslator
# from Languages import *
# import streamlit as st
# import tempfile
# import os

# def translate(src,to,text):
#     translator =GoogleTranslator(source=f"{src}",target=f"{to}")
#     out =translator.translate(f"{text}")
#     return out


# st.title("Translator")
# # st=st.form(key="form1")
# audio_file=st.file_uploader("upload yiur audio file (.wav)",["wav"])
# if st.button("listen",key="3123") and audio_file is not None:
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         temp_file.write(audio_file.read())
#         temp_file_path = temp_file.name
#         # st.write(temp_file_path)
#     st.audio(temp_file_path, format='audio/wav')  # or 'audio/mp3'
#     if st.button("Delete Temporary File"):
#         os.remove(temp_file_path)
#         st.success("Temporary file deleted.")
# src=st.selectbox("From",["arabic","english","spanish","french"],key="src")
# user_input=st.text_area("Enter text")
# target=st.selectbox("To",["arabic","english","spanish","french"],key="trgt")
# b1=st.button("Translate")
# # if b1:
# #     f1.text_area("Result",f"{translate(src,target,user_input)}")



# # m=GoogleTranslator.get_supported_languages(GoogleTranslator())
# # print(m)
# # translator =GoogleTranslator(source="auto",target="arabic")
# # out =translator.translate("hello")
# # print(out)











# langs=['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 
# 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 
# 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']


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

