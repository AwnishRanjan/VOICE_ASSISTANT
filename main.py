import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import urllib.parse
from googlesearch import search
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify client credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id='64f8e1acd26f4ec3978d4aefd85bcd08',
                                                      client_secret='15a841c2c0f14f1d8da30951f8b9402f')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize the speech recognition recognizer
r = sr.Recognizer()

def play_song(query):
    try:
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']

            webbrowser.open(track_uri)
            speak("Playing " + results['tracks']['items'][0]['name'])
        else:
            speak("No results found for " + query)
    except spotipy.SpotifyException:
        speak("Sorry, there was an error playing the song.")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening....")
            r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            audio = r.listen(source, timeout=5)

        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")

        query = query.lower()  # Convert query to lowercase for easier matching

        if "how are you" in query:
            speak("I am good sir... how can I help you")
        elif "sophia" in query:
            speak("Yes sir?")
        elif "time" in query:
            time()
        elif "stop" in query:
            speak("Nice to meet you sir. Have a good day.")
            exit()
        elif "open" in query or "show" in query:
            if "pictures" in query:
                path = r'C:\Users\ranja\Pictures'
                os.startfile(path)
            else:
                website_name = query.split("open" or "show")[-1].strip()
                website_url = "https://" + website_name + ".com"
                website_site = urllib.parse.unquote(website_url)
                webbrowser.open(website_site)
        elif "play" in query or "song" in query:
            result = query.split("play" or "song")[-1].strip()
            play_song(result)
        elif any(keyword in query for keyword in ["what is", "who is", "search"]):
            name = query.split("what is" or "who is" or "search")[-1].strip()
            search_engine = search(name, tld="com", num=1, stop=1, pause=1)
            for result in search_engine:
                result = urllib.parse.urlunsplit(result)
                webbrowser.open(result)
        elif "date of birth" in query:
            speak("Sir, I am just a software. I was invented on June 22, 2023.")
        else:
            speak("Sorry sir, can you repeat that?")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Sorry, My speech recognition service is currently unavailable.")

def time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")

def wish():
    speak("HEY !! THIS IS SOFIA FROM SRM VOICE COMMAND ")

if __name__ == '__main__':
    wish()
    while True:
        take_command()
