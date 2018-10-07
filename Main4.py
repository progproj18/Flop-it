import RPi.GPIO as GPIO
import time
import timeit
import random
import tm1637
import math       #nötig?
import spidev     #nötig?
import os         #nötig?
import Reader
import kp
import Joy

GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)

#Pins:
LedR = 32
LedG = 29
LedB = 35
LedY = 33
LedW = 8
Lichtschranke = 10
#[LedR,LedG,LedB,LedY,LedW,Lichtschranke]=[32,29,35,33,8,10]             #geht das?
GPIO.setup(Lichtschranke, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup([LedW,LedR, LedG, LedB, LedY], GPIO.OUT, initial=GPIO.LOW)
#Variablen:
Startzeit = 0
Zeitlimit = 40
Zeitdauer = 0
Punktestand = 0
Zehner=0

DisplayS = tm1637.TM1637(38,40,2) #2 entspricht Helligkeit
DisplayS.Clear()
#Funktionen
def Score():
    Punktestand = Punktestand+1
    if Punktestand > 9:
        Punktestand =0
        Zehner=Zehner+1
    DisplayS.Show1(3,Punktestand)
    DisplayS.Show1(2, Zehner)               #return nötig?
     
# Endlosschleife
while True:
    
    GPIO.output(LedW, GPIO.HIGH)
    GPIO.wait_for_edge(Lichtschranke, GPIO.RISING)

    DisplayS.Clear()
    
    GPIO.output(LedW, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.LOW)  
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.HIGH)   
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.LOW)
    #Zeit starten:
    Startzeit = timeit.default_timer()
    
    while Zeitdauer <= Zeitlimit:
        x = random.randint(1,4)
            
        if x == 1 :
            GPIO.output(LedR, GPIO.HIGH)
            kp.kp()
            time.sleep(1)                                                   #wofür?
            GPIO.output(LedR, GPIO.LOW)
            Score()
            Zeitdauer = (timeit.default_timer()-Startzeit)
                    
        elif x == 2 :
            GPIO.output(LedG, GPIO.HIGH)
            #wait_for_edge(Lichtschranke,GPIO.RISING)
            while GPIO.input(Lichtschranke) == 0 and Zeitdauer <= Zeitlimit:
                Zeitdauer = (timeit.default_timer()-Startzeit)
            #else:
            while GPIO.input(Lichtschranke) == 1 and Zeitdauer <= Zeitlimit:
                Zeitdauer = (timeit.default_timer()-Startzeit)
            GPIO.output(LedG, GPIO.LOW)
            Score()
            Zeitdauer = (timeit.default_timer()-Startzeit)
            time.sleep(1)                                                #?
        elif x == 3 :
            GPIO.output(LedB, GPIO.HIGH)
            Joy.Joys()       
            GPIO.output(LedB, GPIO.LOW)
            Score()
            Zeitdauer = (timeit.default_timer()-Startzeit)
                    
        elif x == 4 :
            GPIO.output(LedY, GPIO.HIGH)
            Reader.reader()
            GPIO.output(LedY, GPIO.LOW)
            Score()
            Zeitdauer = (timeit.default_timer()-Startzeit)
            time.sleep(0.5)                                                 #?
    Startzeit = 0
    Zeitdauer = 0
    Punktestand = 0
    Zehner=0
