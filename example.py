from pulsesensor import Pulsesensor
import time
import RPi.GPIO as GPIO
import requests
import json


firebase_url = "https://ldr-app-85d9a.firebaseio.com/"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT) #green
GPIO.setup(21,GPIO.OUT) #yellow
GPIO.setup(20,GPIO.OUT) #blue
GPIO.setup(16,GPIO.OUT) #white
GPIO.setup(13,GPIO.OUT) #red


p = Pulsesensor()
p.startAsyncBPM()
bpmArray = []

try:
    while True:
        bpm = p.BPM
        bpmArray.append(bpm)

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

            time.sleep(0.3)
                
except (KeyboardInterrupt, SystemExit):
    print('Manual break by user')
    data = {'bpm': bpmArray}
    result = requests.post(firebase_url + '/' + str(int) + '/bpm.json', data=json.dumps(data))
    print ('Record inserted. Result Code = ' + str(result.status_code) + ',' + result.text)
    raise
except:
    p.stopAsyncBPM()
