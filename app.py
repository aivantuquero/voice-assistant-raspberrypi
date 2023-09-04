import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import pandas as pd


load_dotenv()
openai_secret_key = os.getenv("OPENAI_SECRET_KEY")
openai.api_key=openai_secret_key

df = pd.read_excel('pricelist.xlsx')
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
r.dynamic_energy_threshold = False
# To make the microphone less sensitive, you can adjust the microphone's input volume or use a noise-cancelling microphone. 
# You can also adjust the energy_threshold
# 0-4000 default is 300, 500-1000 is good for noisy environment
r.energy_threshold = 1900
r.phrase_threshold = 0.3
r.pause_threshold = 0.5
r.non_speaking_duration = 0.5
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
    print("Listening for 'hey TBM'...") 

    while True:
        audio = r.listen(source)
        try:
            
            text = r.recognize_whisper_api(audio, api_key=openai_secret_key)
            if "tbm" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

def product_price(source):
    engine.say("okay, what is the product name?")
    engine.runAndWait()

    audio = r.listen(source)

    productName = r.recognize_whisper_api(audio, api_key=openai_secret_key )

    print(f"You said: {productName}")

    # Load the Excel file into a pandas DataFrame
    

    if "-" in productName:
        productName = productName.replace("-", "")


    # Search for the product in the DataFrame
    product = df[df['ProductName'] == productName.upper()]

    # Check if the product was found
    if len(product) == 0:
        engine.say("I can't process what you said. Please speak to the salesperson.")
        engine.runAndWait()
    else:
        # Get the price of the product
        price = product.iloc[0]['Price']
        engine.say(f"The price of {productName} is {price}.")
        engine.runAndWait()




    return 


# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_whisper_api(audio, api_key=openai_secret_key )
            print(f"You said: {text}")

            
            if "price for a certain product" in text.lower() or "price for certain product" in text.lower() or "i need the price for a certain product" in text.lower() or "i need a price for a certain product" in text.lower():
                product_price(source)
                continue



            prefix = "Respond short and cute. Use short sentences. "
            text = prefix + text
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)
    
            print("Listening...")

            # engine.say(response_text)
            # You can also make your Raspberry Pi speak from the Python code. using espeak
            # os.system("espeak ' "+response_text + "'")
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
        except sr.WaitTimeoutError:
            print("Timeout, listening...")
            listen_for_wake_word(source)
            break
        except sr.HTTPError as e:
            print(f"Could not request results from Wit.ai service; {e}")
            engine.say(f"Could not request results from Wit.ai service; {e}")
            engine.runAndWait()
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