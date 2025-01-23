# functions for wea-board
import requests
import time
from colorama import *
from datetime import datetime, timezone

# returns http get request in text
def get_request(url):
    response = requests.get(url)
    time.sleep(0.5)

    if response.status_code == 200:
        return response.text
    else:
        return "Response failed with code: " + str(response.status_code)

def convert_timestamp(timestamp):
    # Parse the timestamp into datetime
    dTime = datetime.fromisoformat(timestamp)
    
    # return the formatted timestamp which is "MM-DD HH:MM:SS"
    return dTime.strftime("%m-%d %H:%M:%S")

# ~~Fix bug that only gets one alert when several are being broadcast.~~
# Comment above can't be fixed as its an API issue ^

# returns alerts from compatible json
def wea_to_array(jsn):
    #vars
    array = []
    headline = ""
    shortTxt = ""
    date = datetime.now(timezone.utc)

    # loop to get alerts from json
    for alert in jsn["alerts"]:
        
        # loop to get alert headlines and WEA 90 Text from alert
        for text in alert["texts"]:
            if text["type"] == "cap_headline":
                headline = text["value"]
            if text["type"] == "cmac_short_text":
                shortTxt = text["value"]
        
        # check if alert has expired to mitigate the api bug
        if date.timestamp() <= datetime.fromisoformat(alert["expires"]).timestamp():
            # push alert to array
            array.append(alert["event"] + " - " + headline + "\n   " + shortTxt + "\n   Time sent: " + convert_timestamp(alert["sent"]) + "\n")
            

    # Return alerts
    return array
