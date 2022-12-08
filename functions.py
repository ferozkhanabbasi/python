from subprocess import run, PIPE
import logging
import speech_recognition as sr
import wave
import contextlib
from flask import logging, Flask, render_template, request
from scipy.io import wavfile
import requests

import os
import gtts
from playsound import playsound
import multiprocessing




headers = {
    'authority': 'api-b2b.backenster.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer a_25rccaCYcBC9ARqMODx2BV2M0wNZgDCEl3jryYSgYZtF1a702PVi4sxqi2AmZWyCcw4x209VXnCYwesx',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://lingvanex.com',
    'referer': 'https://lingvanex.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

def get_language_code(lang):
   if lang=="English":
      code = "en_US"
   if lang=="Spanish":
      code = "es_ES"
   if lang=="Chinese (Simplified)":
      code = "zh-Hans_CN"
   if lang=="Afrikaans":
      code = "af_ZA"
   if lang=="Russian":
      code = "ru_RU"
   if lang=="Filipino":
      code = "tl_PH"
   if lang=="Urdu":
      code = "ur_PK"

   return code


def translateAudio(filename, lang_from, lang_to):
   r=sr.Recognizer()
   with sr.AudioFile(filename) as source:
      audio = r.adjust_for_ambient_noise(source)
      audio_data = r.record(source)
      text = r.recognize_google(audio_data)
      #samplerate, data = wavfile.read('audio.wav')
      #length = data.shape[0] / samplerate
      #print('Lenght',length)
      #res = len(text.split())/length
      #res = str(res*60)

      data = {
         'from': get_language_code(lang_from),
         'to': get_language_code(lang_to),
         'text': str(text),
         'platform': 'dp',
      }
      translated_text = requests.post('https://api-b2b.backenster.com/b1/api/v3/translate/', headers=headers, data=data)
      translated_text = translated_text.json()['result']
      print(translated_text)


      # covert into language
      langs =  gtts.lang.tts_langs()
      lang_code =  list(langs.keys())[list(langs.values()).index(lang_to)]
      print(lang_to, lang_code)
      tts = gtts.gTTS(translated_text, lang=lang_code)
      #tts = gtts.gTTS("Hello world")
      tts.save("data/hola.wav")
      #playsound("hola.mp3")
      #p = multiprocessing.Process(target=playsound, args=("data/hola.wav",))
      #p.start()
   return text, translated_text
