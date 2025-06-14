import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
newsapi = os.getenv("newsapi")
openai.api_key = os.getenv("api_key")

# Text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(cmd):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google."},
            {"role": "user", "content": cmd}
        ]
    )
    return completion.choices[0].message["content"]

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Sure, opening Google.")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Sure, opening Facebook.")
    elif "open instagram" in c or "open insta" in c:
        webbrowser.open("https://instagram.com")
        speak("Sure, opening Instagram.")
    elif "open twitter" in c or "open x" in c:
        webbrowser.open("https://x.com")
        speak("Sure, opening Twitter.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Sure, opening YouTube.")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Sure, opening LinkedIn.")
    elif "open saad.dev" in c:
        webbrowser.open("https://sbkdev.vercel.app")
        speak("Sure, opening Saad.Dev.")
    elif "news" in c:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=pk&apiKey={newsapi}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Optional: Limit to top 5
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news right now.")

    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for wake word...")
                speak("Listening for wake word...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=7, phrase_time_limit=5)
                word = r.recognize_google(audio)

                if "jarvis" in word.lower():
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
            print("Error:", e)
