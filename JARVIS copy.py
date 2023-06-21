# JARVIS - Just A Rather Very Inteligent System

# user defined modules
from utility import (credentials, send_sms, sendEmail, turn_off, turn_on,
                     weather)

# internal modules
import datetime
import os
import random
import webbrowser
from time import sleep as s

# external modules
import pandas as pd
import pyttsx3  # for Text-to-Speech
import pywhatkit  # pip install pywhatkit
import speech_recognition as sr  # for Speech-to-Text
import wikipedia
import wolframalpha  # pip install wolframalpha
from playsound import playsound  # pip install playsound==1.2.2


# reading the Contact details from phonebook.csv
df = pd.read_csv("phonebook.csv")
df.set_index(df.name, inplace=True)
df = df.T

# Directories
SONG_DIR = 'songs\\'
MEDIA_DIR = 'media\\'
VSCODE_DIR = "C:\Program Files\Microsoft VS Code\Code.exe"

# Variables
RESULTS = ""

# Initialising Text to Speech Engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 145)  # Speech Rate


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# First of all greets the user


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Hello sir, Please tell me how may I help you")


# It takes microphone input from the user and returns string output
def takeCommand():

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Sorry, can you say that again please?")
        return "None"
    return query


# this Function get called after "Hey Jarvis", "Ok Jarvis" or "Wake up" user voice input
def wake_up():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Z", end="", flush=True)
        audio = r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=2)
    try:
        print("zz", end=" ", flush=True)
        query = r.recognize_google(audio, language="en-IN")

    except Exception as e:
        return "None"
    return query


def main():

    silence = 0
    while silence < 5:
        # query is the string returnd by the takeCommand function which is converted into text by user input speech
        query = takeCommand().lower()

        if query == "none":
            silence += 1

        else:
            silence = 0

            # Logics for executing tasks based on query
            if "hello" in query:
                speak("Hello Sir, How may I help you?")

            elif "how are you" in query:
                msgs = ["I am fine sir!, thanks for asking... "]
                speak(random.choice(msgs))

            elif "nothing" in query or "abort" in query or "bye" in query or "quit" in query:
                speak("okay")
                speak("Bye Sir, have a good day.")
                break

            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia ")
                print(results)
                speak(results)

            elif "open youtube" in query:
                speak("okay")
                webbrowser.open("www.youtube.com")

            elif "open google" in query:
                speak("okay")
                webbrowser.open("www.google.co.in")

            elif "open stack overflow" in query:
                speak("okay")
                webbrowser.open("www.stackoverflow.com")

            elif "play music" in query:
                speak("Okay. Playing")
                song_dir = SONG_DIR
                songs = os.listdir(song_dir)
                os.startfile(os.path.join(
                    song_dir, songs[random.randint(0, len(songs)-1)]))

            elif "stop music" in query:
                os.system('taskkill /im wmplayer.exe /f')

            elif "play" in query:
                speak("Okay. Playing!")
                pywhatkit.playonyt(query.split("play")[1])

            elif "the time" in query:
                speak("okay")
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
                print(f"Sir, the time is {strTime}")

            elif "open code" in query:
                speak("okay")
                os.startfile(VSCODE_DIR)

            elif "email" in query:
                speak("Who is the recipient? ")
                recipient = takeCommand()
                recipient = df.get(recipient)
                print(recipient)

                try:
                    speak("What should I say?")
                    content = takeCommand()
                    sendEmail(df.get(recipient).get("email"), content)
                    speak("Your email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry Sir! I am unable to send your e-mail")

                """  
                elif "send message" in query:

                    speak("Who is the recipient? ")
                    recipient = takeCommand()
                    print(df.get(recipient))

                    if to!= None:
                        speak("okay... What should I say?")
                        message = takeCommand()
                        speak("Okay... Sending...")
                        speak(send_sms(message, df.get(recipient).get("number")))
                    
                    else:
                        speak("sorry sir, May be this contact is not in our phonebook, can you please tell me the number?")
                        number = takeCommand()
                        speak("okay... What should I say?")
                        message = takeCommand()
                        speak("Okay... Sending...")
                        speak(send_sms(message, number.replace(" ","")))
                    """

            elif "turn on light" in query:
                speak(turn_on("light"))

            elif "turn off light" in query:
                speak(turn_off("light"))

            elif "turn on fan" in query:
                speak(turn_on("fan"))

            elif "turn off fan" in query:
                speak(turn_off("fan"))

            elif "weather today" in query:
                speak(weather())

            elif "send this to" in query:
                to = query.split("to")[1].strip()
                sendEmail(df.get(to).get("email"), RESULTS)
                speak("Email has been sent!")
                RESULTS = ''

            else:
                # Put your Wolframalpha Authorization Key
                client = wolframalpha.Client(
                    credentials.get("wolframalphaKey"))
                speak("Searching...")
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    RESULTS = f"Here are some results according to \n'{query}'.\n\nResult: {results}"
                    speak("Got it.")
                    speak("Google says - ")
                    print(results)
                    speak(results.replace("|", " "))

                except:
                    speak("Sorry, Can you say that again please")

                    # speak("Here are some results...")
                    # webbrowser.open(
                    #     "https://www.google.com/search?client=firefox-b-d&q="+query.replace(" ", "+"))

    print("\nSleeping...")


if __name__ == "__main__":
    # playsound(f"{MEDIA_DIR}wake_up.wav")
    playsound(r"G:\\charudatt\\JARVIS\Source Code\\media\wake_up.wav")
    wishMe()
    main()

    while True:
        # query is the string returnd by the takeCommand function which is converted into text by user input speech
        query = wake_up().lower()
        if "ok jarvis" in query or "wake up" in query or "Hey jarvis":
            playsound(f"{MEDIA_DIR}wake_up.wav")
            main()
        elif "nothing" in query or "abort" in query or "bye" in query or "quit" in query:
            speak("OK Bye, Have a nice day")
            exit()
