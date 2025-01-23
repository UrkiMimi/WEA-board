import json
import time
import os
import pygame
import traceback
from functions import *

# TODO 1: Seperate python file so its easier to debug.

# region vars
json_url = "https://nmknkohb83.execute-api.us-east-1.amazonaws.com/prod/warn_out/?status=active"
refresh_time = 5
oldAlerts = []

#audio manager
pygame.mixer.init()
snd = pygame.mixer.Sound("assets/tock.wav")



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
        print(Fore.BLUE + "Active alerts: \n ")
        for i in range(len(alerts)): # loop for pushing alerts to console
            print(Fore.RESET + str(i+1) + ". " + alerts[i])
        
        # make sound if new alert is added to alert board
        if oldAlerts != alerts:
            snd.play()

        # refresh part 1
        oldAlerts = alerts
    except:
        # bruh
        os.system("clear")
        print(Fore.RED) # change text coolor to red
        traceback.print_exc()
        break

    # refresh part 2
    taskStopTime = time.time()
    print("\nTime to process: " + str(round(taskStopTime - taskStartTime,3)))

    # stopgap to set refresh speed to 1 if its shorter than a second
    if refresh_time <= 1:
        refresh_time = 1
    
    time.sleep(refresh_time)