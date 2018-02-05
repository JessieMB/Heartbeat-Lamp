from pulsesensor import Pulsesensor
import time
import RPi.GPIO as GPIO
import requests
import json
import itertools

#Can't get Firebase package installed on Raspbian; working around using requests

firebase_url = "https://ldr-app-85d9a.firebaseio.com/%3Ctype%20'int'%3E/bpm/-L4UczUZraRXeAY6l2m7/bpm.json?print=pretty&format=export&download=ldr-app-85d9a-bpm-export.json"
r = requests.get(firebase_url)
pulseArray = ""
for x in r:
    pulseArray = x
    print(x)
data = json.loads(pulseArray)
userBPM = []
for x in data:
    userBPM.append(int(x))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT) #green
GPIO.setup(21,GPIO.OUT) #yellow
GPIO.setup(20,GPIO.OUT) #blue
GPIO.setup(16,GPIO.OUT) #white
GPIO.setup(13,GPIO.OUT) #red


p = Pulsesensor()
p.startAsyncBPM()
try:
    while True:

        for bpm in userBPM:

            if bpm >= 30 and bpm < 75: #blue
                GPIO.output(20,GPIO.HIGH)
                time.sleep(bpm * .075)
                GPIO.output(20,GPIO.LOW)
                time.sleep(bpm * .075)


            elif bpm >= 75 and bpm < 95: #green
                GPIO.output(19,GPIO.HIGH)
                time.sleep(bpm * .005)
                GPIO.output(19,GPIO.LOW)
                time.sleep(bpm * .005)


            elif bpm >= 95: #red
                GPIO.output(13,GPIO.HIGH)
                time.sleep(bpm * .005)
                GPIO.output(13,GPIO.LOW)
                time.sleep(bpm * .005)

            else:
                GPIO.output(21,GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(16,GPIO.HIGH)
                GPIO.output(21,GPIO.LOW)
                time.sleep(.2)
                GPIO.output(16,GPIO.LOW)

                time.sleep(0.5)

except (KeyboardInterrupt, SystemExit):
    print('Manual break by user')
    p.stopAsyncBPM
    raise
except:
    p.stopAsyncBPM()
