import os
from time import sleep as s
import pickle

def getCredentials():
    try:
        with open('credentials.pickle', 'rb') as f:
            credentials = pickle.load(f)
        return credentials
    except FileNotFoundError as e:
        return False

try:
    import pandas as pd

except:
    for i in "Building JARVIS... It may take some time. please wait a moment!":
        print(i, end="", flush=True)
        s(0.05)
    try:
        os.system(r"pip install -r .\\requirements.txt")
        os.system("pip install -Iv pyttsx3==2.6 -U")
        os.system(f"pipwin refresh")
        os.system(f"pipwin install pyaudio==0.2.11")
    except Exception as e:
        print(e)
    else:
        print("\nSetup has been Completed... JARVIS is now Ready-to-Use.\n")

finally:
    credentials = getCredentials()
    while not credentials or credentials is None:
        print(f"""
    {'-'*100}
    Please set your API Keys first. If you don't have API Authorizations then get it from links given below

    ● Email - You must create an App password. 
        Going to Google account (https://myaccount.google.com/) > Security tab > 2 Step Verification.
        After active 2 Step Verification, a new option under "Signing in to Google" the "App passwords" option will be activated. 
        Just create one app password and use as password to authenticate.

    ● Fast2SMS API - Get your API Authorization Key here https://docs.fast2sms.com/?python#post-method13 

    ● OpenWeatherMap API - Get your API Authorization Key here https://developer.accuweather.com/

    ● Wolframapha API - Get your API Authorization Key here https://products.wolframalpha.com/api/
    {'-'*100}
    """)

        set_credentials = {"fast2smsKey": input("Enter Your Fast2Sms API Key : ").strip(),
                           "openweathermapKey": input("Enter Your OpenWeatherMap API Key : ").strip(),
                           "wolframalphaKey": input("Enter Your WolframAlpha API Key : ").strip(),
                           "email": {"id": input("Enter Your Email ID : ").strip(), "password": input("Enter Your Email App Password : ").strip()},
                           "registered": True}

        with open('credentials.pickle', 'wb') as f:
            pickle.dump(set_credentials, f)

        credentials = getCredentials()

        # credentials.get("fast2smsKey")
        # credentials.get("openweathermapKey")
        # credentials.get("wolframalphaKey")
        # credentials.get("email").get("id")
        # credentials.get("email").get("password")
        # credentials.get("status")

        # fast2sms = "IcfdlOibxr5tXa6w0qez3h4uLQsMEVT2ARJUKWYN8DGPF9omv1yxNs0gn8Dtc6rXjLh37pqiIfMCYUSw"
        # openWeatherMap = "9cc05b3f33eed1315831481525fdfcdd"
        # wolframalpha = "3L78QV-9W42VJ8642"

        # email = "download.charudatt@gmail.com"
        # password = "ytnkofofuliilctv"
