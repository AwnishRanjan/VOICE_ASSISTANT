import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import urllib.parse
import spotipy
from googlesearch import search
import os
import spotipy as sp

from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='64f8e1acd26f4ec3978d4aefd85bcd08',
                                                      client_secret='15a841c2c0f14f1d8da30951f8b9402f')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def play_song(query):
    try:
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']

            webbrowser.open(track_uri)
            speak("Playing " + results['tracks']['items'][0]['name'])
            take_command()
        else:
            speak("No results found for " + query)
            take_command()
    except spotipy.SpotifyException:
        speak("Sorry, there was an error playing the song.")
        take_command()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 5
        audio = r.listen(source, phrase_time_limit=3, timeout=0.6)

    try:
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        query = query.split("hi")[-1]
        if "how are you" in query:
            speak("i am good sir...how can I help you")
            take_command()
        elif "sophia" in query:
            speak("yes sir")
            take_command()
        elif "time" in query:
            time()
            take_command()
        elif "stop" in query:
            speak(f"nice to meet you sir .. have a good day")
            return exit()

        #   opening websites
        elif "open" or "show" in query:
            if "open pictures" in query:
                path = r'C:\Users\ranja\Pictures'
                os.startfile(path)
                return take_command()

            website_name = query.split("open")[-1].strip()
            website_url = "https://" + website_name + ".com"
            #  to remove %20 means space  in url ::: use urllib
            website_site = urllib.parse.unquote(website_url)
            webbrowser.open(website_site)

        elif "play" or "song" in query:
            result = query.split("play" or "song")[-1].strip()
            play_song(result)
            take_command()

        elif "search" or "what is" or "who is" in query:
            name = query.split("what is" or "who is" or "search")[-1].strip()
            search_engine = search(name, tld="com", num=1, stop=1, pause=1)
            for result in search_engine:
                result = urllib.parse.urlunsplit(result)
                webbrowser.open(result)
                return exit()

        elif "date of birth" in query:
            speak("sir i am just a software .... I was invented on  twenty second of june 2023")
            take_command()
        else:
            speak("sorry sir can you repeat again..")
            take_command()

    except sr.UnknownValueError:
        # speak("")
        return take_command()

    except sr.RequestError:
        speak("Sorry, sir My speech recognition service is currently unavailable.")
        return None


def time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")
    take_command()


def wish():
    now = datetime.datetime.now()
    speak("Good day! This is Sophia, your dedicated voice assistant.... How may I be of service to you today?")


if __name__ == '__main__':
    wish()
    while True:
        take_command()
