import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

mytext = 'Welcome to me'
language = 'en'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
openai.api_key='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'
load_dotenv()
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
greetings = [f"Howdy, partner! What can I do for you today?",
             "Hello, there! What can I do for you today?",
             "Hey, what's up? What can I do for you today?",
             f"Aloha! You're looking great today. What can I do for you today?",
             f"Hi, why are you so good looking? What can I help you?" ]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source,timeout=1,phrase_time_limit=10)
        try:
            
            text = r.recognize_whisper_api(audio, api_key='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')
            if "bubble" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_whisper_api(audio, api_key='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' )
            print(f"You said: {text}")
            prefix = "respond like a cute little robot. "
            text = prefix + text
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)
    
            print("speaking")

            # engine.say(response_text)
            # You can also make your Raspberry Pi speak from the Python code. using espeak
            # os.system("espeak ' "+response_text + "'")
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)