# user defined modules
from setup import credentials

# internal modules
import datetime
import json
import smtplib

# external modules 
import requests
from plyer import notification
from pyfirmata import Arduino, util  # for Serial Communication with Arduino

# Email Service----------------------------



def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # put server.login(yourEmailID, appPassword) as an argument
    server.login(credentials.get("email").get("id"), credentials.get("email").get("password"))
    message = f"Subject: From - JARVIS\n\n{content}"
    # put server.sendmail(yourEmailId, to, message)
    server.sendmail(credentials.get("email").get("id"), to, message)
    server.close()


# Message Service----------------------------

def send_sms(message, mob_no):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=" + message + \
        "&language=english&route=p&numbers=" + mob_no + ""
    headers = {
        'authorization': credentials.get("fast2smsKey"),
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }  # Put your fast2sms API Authorization tocken in "authorization"
    response = requests.request("POST", url, data=payload, headers=headers)
    status = json.loads(response.content.decode('utf-8')).get("message")
    print(*status)
    return("".join(status))


# Weather Service----------------------------

def weather():
    city = "Bhusawal"
    # Paste Your OpenWeatherMap API Key Here
    api = credentials.get("openweathermapKey") 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"

    r = requests.get(url).json()
    time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        name = r["name"]
        temp = int(r["main"]["temp"] - 273.15)
        weather = r["weather"][0]["main"]
        print(
            f"Temperature : {str(temp)} degrees\nWeather : {weather} in {name}\nTime : time is {time}")
        return(f"its {str(temp)} degrees and {weather} in {name}, time is {time}")

    except Exception as e:
        pass


# Serial Communication with Arduino----------------------------

devices = {"light": 13, "fan": 12}

# Defining Arduino Port
try:
    # Ensure Your Serial Communication Port and put that here as an argument like "COM4"
    board = Arduino("COM6")
    board.digital[12].write(0)
    board.digital[13].write(0)
except:
    print("Currently the Arduino is not connected to our system")
    notification.notify(title="JARVIS - Arduino Board Not Found",
                        message="Arduino Board is not connected to our system",
                        app_icon="media\\arduino.ico",
                        timeout=10)


def turn_on(device):
    pin = devices.get(device)
    try:
        board.digital[pin].write(1)
        print(f"{device} is now turned on...")
        return f"{device} is now turned on..."

    except Exception as e:
        print(e)
        print("Sorry, Currently the Arduino is not connected to our system")
        return ("Sorry, Currently the Arduino is not connected to our system")


def turn_off(device):
    pin = devices.get(device)
    try:
        board.digital[pin].write(0)
        print(f"{device} is now turned off...")
        return f"{device} is now turned off..."
    except Exception as e:
        print(e)
        print("Sorry, Currently the Arduino is not connected to our system")
        return ("Sorry, Currently the Arduino is not connected to our system")
