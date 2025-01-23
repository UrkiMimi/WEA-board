import json
import requests
import time
import os
import pygame
import traceback

# TODO 1: Seperate python file so its easier to debug.

# region vars
json_url = "https://nmknkohb83.execute-api.us-east-1.amazonaws.com/prod/warn_out/?status=active"
refresh_time = 5
oldAlerts = []

#audio manager
pygame.mixer.init()
snd = pygame.mixer.Sound("tock.wav")



# region functions
# TODO 2: Fix bug that only gets one alert when several are being broadcast.
# returns http response in text
def get_request(url):
    response = requests.get(url)
    time.sleep(0.5)

    if response.status_code == 200:
        return response.text
    else:
        return "Response failed with code: " + str(response.status_code)

# returns alerts from compatible json
def wea_to_array(jsn):
    array = []
    headline = ""
    shortTxt = ""

    # loop to get alerts from json
    for alert in jsn["alerts"]:
        
        # loop to get alert headlines and WEA 90 Text from alert
        for text in alert["texts"]:
            if text["type"] == "cap_headline":
                headline = text["value"]
            if text["type"] == "cmac_short_text":
                shortTxt = text["value"]
        
        # Add alert to array
        array.append(alert["event"] + " - " + headline + "\n  " + shortTxt)

    # Return alerts
    return array


# region main loop
while True:
    #init
    taskStartTime = time.time()

    # so the program doesnt crash and burn when it gets an invalid json
    try:
        # get alertJSON from http request and converts the JSON into a somewhat friendly 
        # display format
        alertJsn = json.loads(get_request(json_url))
        alerts = wea_to_array(alertJsn)

        # push alerts to console
        os.system("clear")
        print("Active alerts: \n ")
        for i in range(len(alerts)): # loop for pushing alerts to console
            print(str(i+1) + ". " + alerts[i])
        
        # make sound if new alert is added to alert board
        if oldAlerts != alerts:
            snd.play()

        # refresh part 1
        oldAlerts = alerts
    except:
        # bruh
        os.system("clear")
        print("JSON isn't valid. \nFull error:\n")
        traceback.print_exc()

    # refresh part 2
    taskStopTime = time.time()
    print("\nTime to process: " + str(round(taskStopTime - taskStartTime,3)))
    time.sleep(refresh_time)