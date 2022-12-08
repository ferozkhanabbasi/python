import cv2, os
import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import functions
import tempfile
import soundfile
import moviepy.editor as mp
from io import StringIO

def main_loop():
    image = Image.open('images/Fome-Ai.png')
    st.sidebar.image(image, width=120)
    st.sidebar.title("ACCENT TRANSLATOR")
    st.title("Accent Translator")
    st.write("AI-powered software for fast and accurate video translation and dubbing into other languages.")
    lang_from = st.sidebar.selectbox('Orignol Language', ('English', 'Spanish', 'Chinese (Simplified)','Afrikaans','Russian','Urdu', 'Filipino' ))
    st.write('Language From:', lang_from)
    lang_to = st.sidebar.selectbox('Translate into Lenguage', ('Spanish', 'English', 'Chinese (Simplified)','Afrikaans', 'Russian','Urdu', "Filipino" ))
    st.write('Language To:', lang_to)
    uploaded_file = st.sidebar.file_uploader("Upload an Audio or Video", type=['mp3', "mp4", "wav", "mov"])
    if uploaded_file is not None:
        #st.title("Translator")
        st.write("File Name: ", uploaded_file)

        # Get Audio from Video
        if uploaded_file.type == 'video/mp4' or uploaded_file.type=="video/quicktime":
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            my_clip = mp.VideoFileClip(tfile.name)
            my_clip.audio.write_audiofile(r"data/my_result.wav")
            file = "data/my_result.wav"
        else:
            data, samplerate = soundfile.read(uploaded_file)
            soundfile.write('data/my_result.wav', data, samplerate, subtype='PCM_16')
            file = "data/my_result.wav"

        text, translated_text = functions.translateAudio(file, lang_from, lang_to)
        if uploaded_file.type != 'video/mp4':
            # print(text)
            st.write("Download Orignol Audio")
            audio_file1 = open(file, 'rb')
            audio_bytes1 = audio_file1.read()
            st.audio(audio_bytes1, format='audio/wav')
     
            st.write("Download "+ lang_to+ " Audio")
            audio_file2 = open('data/hola.wav', 'rb')
            audio_bytes2 = audio_file2.read()
            st.audio(audio_bytes2, format='audio/wav')

        if uploaded_file.type == 'video/mp4' or uploaded_file.type=="video/quicktime":
            audio = mp.AudioFileClip('data/hola.wav')
            final_video = my_clip.set_audio(audio)
            #Extracting final output video
            final_video.write_videofile("data/output_video.mp4")
            video_file1 = open("data/output_video.mp4", 'rb')
            video_bytes1 = video_file1.read()
            st.video(video_bytes1)

if __name__ == '__main__':
    main_loop()