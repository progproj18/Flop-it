import RPi.GPIO as GPIO
import time
import timeit
import random
import tm1637
import math
import spidev
import os
import Reader
import kp
import Joy

GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)

#Pins:
LedR = 32  #x=1 (21)<--in Klammern die GPIO-Pinnummern
LedG = 29  #x=2 (20)
LedB = 35  #x=3 (26)
LedY = 33  #x=4 (16)
LedW = 8  #(19) Led am Startbutton
#Start_Button = 27 #(13)
#Joystick = 12     #(12)    Die Buttons repraesentieren besagte Stationen
Lichtschranke = 10#(6) 
#Keypad = 15       #(5) 
Kartenleser = 16  #(7) #Aus-/Eingaenge:
#GPIO.setup(LedR, GPIO.OUT)
#GPIO.setup(LedG, GPIO.OUT)
#GPIO.setup(LedB, GPIO.OUT)
#GPIO.setup(LedY, GPIO.OUT)
#GPIO.setup(LedW, GPIO.OUT)

#GPIO.setup(Start_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #legt Ausgangszustand auf Low(0) fest
#GPIO.setup(Joystick, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(Keypad, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Lichtschranke, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(Kartenleser, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Variablen:
Startzeit = 0
Zeitlimit = 40
Zeitdauer = 0
Punktestand = 0
Zehner=0
#GPIO.output(LedW, GPIO.LOW)
#GPIO.output(LedR, GPIO.LOW)
#GPIO.output(LedG, GPIO.LOW)
#GPIO.output(LedB, GPIO.LOW)
#GPIO.output(LedY, GPIO.LOW)
GPIO.setup([LedW,LedR, LedG, LedB, LedY], GPIO.OUT, initial=GPIO.LOW)
#Funktionen

 
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)

# Endlosschleife
while True:
    if GPIO.input(Lichtschranke) == 0:
        print ("an")

    DisplayS = tm1637.TM1637(38,40,2) #2 entspricht helligkeit
    
    #anzeige = [1,2,3,4]
    #Display.Show(anzeige)
    #print ("1234  - Taste bitte")
    #scrap = input()

    #Display.Show1(1, 5)
    #Display.Show1(2, 4)

    #print ("1544  - Taste bitte")
    #scrap = input()

    #Display.ShowDoublepoint(True)
    #Display.SetBrightnes(4)

    #print ("15:40  heller - Taste bitte")
    #scrap = input()

    #Display.Clear()

    GPIO.output(LedW,     GPIO.HIGH)
    GPIO.wait_for_edge(Lichtschranke, GPIO.RISING)
   #if GPIO.input(Start_Button) == 1:
    DisplayS.Clear()
    GPIO.output(LedW, GPIO.LOW)# Ausschalten, optional: countdown+buzzer    
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.HIGH)# Ausschalten, optional: countdown+buzzer    
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.LOW)# Ausschalten, optional: countdown+buzzer    
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.HIGH)# Ausschalten, optional: countdown+buzzer    
    time.sleep(0.5)
    GPIO.output(LedW, GPIO.LOW)
    #Zeit starten:
    Startzeit = timeit.default_timer()
    while Zeitdauer <= Zeitlimit:
        x = random.randint(1,4)
            
        if x == 1 :
            GPIO.output(LedR, GPIO.HIGH)
            kp.kp()
            time.sleep(1)
            GPIO.output(LedR, GPIO.LOW)
            
            #if Zeitdauer <= Zeitlimit:
            Punktestand = Punktestand+1
                
            if Punktestand > 9:
                Punktestand =0
                Zehner=Zehner+1
                DisplayS.Show1(3, Punktestand)
                DisplayS.Show1(2, Zehner)
            DisplayS.Show1(3,Punktestand)
            DisplayS.Show1(2, Zehner)
            Zeitdauer = (timeit.default_timer()-Startzeit)
                    
        elif x == 2 :
            GPIO.output(LedG, GPIO.HIGH)
            while GPIO.input(Lichtschranke) == 0 and Zeitdauer <= Zeitlimit:
                    Zeitdauer = (timeit.default_timer()-Startzeit)
            else:
                GPIO.output(LedG, GPIO.LOW)
                
                #if Zeitdauer <= Zeitlimit:
                Punktestand = Punktestand+1
                
                if Punktestand > 9:
                    Punktestand = 0
                    Zehner = Zehner + 1
                    DisplayS.Show1(3, Punktestand)
                    DisplayS.Show1(2, Zehner)
                DisplayS.Show1(3,Punktestand)
                DisplayS.Show1(2, Zehner)
                Zeitdauer = (timeit.default_timer()-Startzeit)
                time.sleep(1)    
        elif x == 3 :
            GPIO.output(LedB, GPIO.HIGH)
            Joy.Joys()       
            GPIO.output(LedB, GPIO.LOW)
            
            #if Zeitdauer <= Zeitlimit:
            Punktestand = Punktestand+1
                
            if Punktestand > 9:
                Punktestand =0
                Zehner=Zehner+1
                DisplayS.Show1(3, Punktestand)
                DisplayS.Show1(2, Zehner)
            DisplayS.Show1(3,Punktestand)
            DisplayS.Show1(2, Zehner)
            Zeitdauer = (timeit.default_timer()-Startzeit)
                    
        elif x == 4 :
            GPIO.output(LedY, GPIO.HIGH)
            #while GPIO.input(Kartenleser) == 0 and Zeitdauer <= Zeitlimit:
            #Zeitdauer = (timeit.default_timer()-Startzeit)
            Reader.reader()
            #else:
            GPIO.output(LedY, GPIO.LOW)
                
                #if Zeitdauer <= Zeitlimit:
            Punktestand = Punktestand+1
                
            if Punktestand > 9:
                Punktestand =0
                Zehner=Zehner+1
                DisplayS.Show1(3, Punktestand)
                DisplayS.Show1(2, Zehner)
            DisplayS.Show1(3,Punktestand)
            DisplayS.Show1(2, Zehner)
            Zeitdauer = (timeit.default_timer()-Startzeit)
            time.sleep(0.5)
    Startzeit = 0
    Zeitdauer = 0
    Punktestand = 0
    Zehner=0


  
# Bisher Probleme/ was fehlt: Das Programm funktioniert nur einmal, danach
# reagiert es auf den Startknopf nichtmehr.(geloest!) EIn Highscore wird noch nicht gezaehlt,
# kein Buzzer drin, kein Led Ring oder 7-Segment-Anzeige. Die Buttons simulieren
# die Stationen und koennen u.U. spaeter durch Funktionen, die man aufruft
# ersetzt werden(?)

