import speech_recognition as sr
import webbrowser
import pyttsx3
 
recognizer = sr.Recognizer()
engine = pyttsx3.init()
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

newsapi = os.getenv("newsapi")

def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiprocess(cmd):
    client = OpenAI(
    api_key=os.getenv("api_key")
    )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"You are a virtual assistant named jarvis skilled in general tasks like alexa and google."},
        {"role":"user","content":cmd}
    ]
    )
    return completion.choices[0].message.content



def processCommand(c):
    c = c.lower()
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("sure opening")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("sure opening")

    elif "open instagram" in c.lower() or "open insta" in c.lower():
        webbrowser.open("https://instagram.com")
        speak("sure opening")

    elif "open twitter" in c.lower() or "open x" in c.lower():
        webbrowser.open("https://x.com")
        speak("sure opening")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("sure opening")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("sure opening")

    elif "open Saad.Dev" in c.lower():
        webbrowser.open("https://sbkdev.vercel.app")
        speak("sure opening")
    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=pk&apiKey={newsapi}")
        if response.status_code ==200:
            data = response.json()
            articles = data.json('articles',[])
            for article in articles:
                speak(article['title'])
    else:
       output= aiprocess(c)
       speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis......")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for wake word....")
                speak("Listening for wake word....")
                
                r.adjust_for_ambient_noise(source, duration=1)  # ✅ Reduce background noise
                audio = r.listen(source, timeout=7, phrase_time_limit=5)
                word = r.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes, how can I assist you today?")
                    with sr.Microphone() as source:
                        print("Jarvis Active.... Listening for command")
                        speak("Jarvis Active.... Listening for command")
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio = r.listen(source, timeout=7, phrase_time_limit=5)
                        command = r.recognize_google(audio)
                        print("Command:", command)
                        processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
