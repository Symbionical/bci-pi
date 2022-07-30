import RPi.GPIO as GPIO
from preferredsoundplayer import *
import time
import bluepy.btle as btle #needs to be linux

def psychra_pump_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)

def psychra_activate_pump():
    GPIO.output(4, GPIO.HIGH)

def psychra_deactivate_pump():
    GPIO.output(4, GPIO.LOW)

def psychra_stimulate():
    for i in range(46):
        psychra_activate_pump()
        print("breathe in " + str(i))
        time.sleep(8)
        print("breathe out " + str(i))
        time.sleep(12)

def stimulate_all():
    stimulate_tES()
    stimulate_pink_noise()

def stimulate_pink_noise():
    print("playing pink noise")
    soundplay("pink_noise.mp3")

def stimulate_tES():
    print("running tES")
    focus1 = btle.Peripheral("B4:99:4C:4F:88:84") #specific for each focus device,
    service1 = focus1.getServiceByUUID("0000AAB0-F845-40FA-995D-658A43FEEA4C")
    characteristic1 = service1.getCharacteristics()[0]
    characteristic1.write((bytes([2, 7, 5, 0, 0, 0]))) # third number in the sequence is the program number on the focus 
    