import csv
import RPi.GPIO as GPIO
from preferredsoundplayer import *
import time
from datetime import datetime
from datetime import date
import bluepy.btle as btle #needs to be linux
from brainflow.data_filter import DataFilter
from csv import writer
import numpy as np

# stimulation legend: 1 = air pump, 2 = pink noise, 3 = tES

def psychra_pump_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)

def psychra_activate_pump():
    GPIO.output(4, GPIO.HIGH)

def psychra_deactivate_pump():
    GPIO.output(4, GPIO.LOW)

def psychra_stimulate():
    log_stim(1)
    for i in range(46):
        psychra_activate_pump()
        print("breathe in " + str(i))
        time.sleep(8)
        psychra_deactivate_pump()
        print("breathe out " + str(i))
        time.sleep(12)

def pre_psychra_stimulate():
    print("Recording Baseline, stimulation in 7 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 6 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 5 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 4 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 3 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 2 minutes")
    time.sleep(60)
    print("Recording Baseline, stimulation in 1 minute")
    time.sleep(60)
    psychra_stimulate()

def stimulate_all():
    stimulate_pink_noise()
    stimulate_tES()

def stimulate_pink_noise():
    print("playing pink noise")
    soundplay("pink_noise.mp3")
    log_stim(2)

def stimulate_tES():
    print("trying tES")

    try:
        focus1 = btle.Peripheral("B4:99:4C:4F:84:AC") #specific for each focus device,
        service1 = focus1.getServiceByUUID("0000AAB0-F845-40FA-995D-658A43FEEA4C")
        characteristic1 = service1.getCharacteristics()[0]
        characteristic1.write((bytes([2, 7, 5, 0, 0, 0]))) # third number in the sequence is the program number on the focus
        print("running tES")
        log_stim(2)
    except:
        try:
            focus1 = btle.Peripheral("B4:99:4C:4F:84:AC") #specific for each focus device,
            service1 = focus1.getServiceByUUID("0000AAB0-F845-40FA-995D-658A43FEEA4C")
            characteristic1 = service1.getCharacteristics()[0]
            characteristic1.write((bytes([2, 7, 5, 0, 0, 0]))) # third number in the sequence is the program number on the focus
            print("running tES")
            log_stim(2)
        except:
            pass

def log_stim(_log_code):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    stimlog = [_log_code, ts]
    today = str(date.today())
    with open(r'stimlog.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(stimlog)