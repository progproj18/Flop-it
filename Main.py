
import RPi.GPIO as GPIO
import time
import random
import tm1637_1
import Joystick_Funktion

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinnummern, alternativ GPIO.BCM für GPIO-Nummerierung
#Pins:
LedR = 3  #x=1 (21)<--in Klammern die GPIO-Pinnummern
LedG = 5  #x=2 (20)
LedB = 7  #x=3 (26)
LedY = 8  #x=4 (16)
LedW = 10  #(19) Led am Startbutton
Start_Button = 11 #(13)
Joystick = 12     #(12)    Die Buttons repräsentieren besagte Stationen
Lichtschranke = 13#(6) 
Keypad = 15       #(5) 
Kartenleser = 16  #(7) #Aus-/Eingänge:
GPIO.setup(LedR, GPIO.OUT)
GPIO.setup(LedG, GPIO.OUT)
GPIO.setup(LedB, GPIO.OUT)
GPIO.setup(LedY, GPIO.OUT)
GPIO.setup(LedW, GPIO.OUT)
GPIO.setup(Start_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #legt Ausgangszustand auf Low(0) fest
GPIO.setup(Joystick, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Keypad, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Lichtschranke, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Kartenleser, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Variablen:
Startzeit = 0
Zeitlimit = 20
Zeitdauer = 0
Punktestand = 0
Zehner=0
GPIO.output(LedW, GPIO.LOW)
#GPIO.output(18, GPIO.LOW)
#Funktionen

# Endlosschleife
while True:
    if GPIO.input(Lichtschranke) == 0:
        print ("an")

    Display = tm1637_1.TM1637(23,24,2) #2 entspricht helligkeit
    
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

    GPIO.output(LedW, GPIO.HIGH)
    GPIO.wait_for_edge(Start_Button, GPIO.RISING)
   #if GPIO.input(Start_Button) == 1:
    Display.Clear()
    GPIO.output(LedW, GPIO.LOW)# Ausschalten, optional: countdown+buzzer    
    #Zeit starten:
    Startzeit = time.clock()
    while Zeitdauer <= Zeitlimit:
        x = random.randint(1,4)
            
        if x == 1 :
            GPIO.output(LedR, GPIO.HIGH)
            while GPIO.input(Joystick) == 0 and Zeitdauer <= Zeitlimit:
                #Zeit messen:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedR, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                if Zeitdauer <= Zeitlimit:
                    Punktestand = Punktestand+1
                
                if Punktestand > 9:
                    Punktestand =0
                    Zehner=Zehner+1
                    Display.Show1(3, Punktestand)
                    Display.Show1(2, Zehner)
                Display.Show1(3,Punktestand)
                Display.Show1(2, Zehner)
                    
        elif x == 2 :
            GPIO.output(LedG, GPIO.HIGH)
            while GPIO.input(Lichtschranke) == 0 and Zeitdauer <= Zeitlimit:
                    Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedG, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                if Zeitdauer <= Zeitlimit:
                    Punktestand = Punktestand+1
                
                if Punktestand > 9:
                    Punktestand = 0
                    Zehner = Zehner + 1
                    Display.Show1(3, Punktestand)
                    Display.Show1(2, Zehner)
                Display.Show1(3,Punktestand)
                Display.Show1(2, Zehner)
                    
        elif x == 3 :
            GPIO.output(LedB, GPIO.HIGH)
            while GPIO.input(Keypad) == 0 and Zeitdauer <= Zeitlimit:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedB, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                if Zeitdauer <= Zeitlimit:
                    Punktestand = Punktestand+1
                
                if Punktestand > 9:
                    Punktestand =0
                    Zehner=Zehner+1
                    Display.Show1(3, Punktestand)
                    Display.Show1(2, Zehner)
                Display.Show1(3,Punktestand)
                Display.Show1(2, Zehner)
                    
        elif x == 4 :
            GPIO.output(LedY, GPIO.HIGH)
            while GPIO.input(Kartenleser) == 0 and Zeitdauer <= Zeitlimit:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedY, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                if Zeitdauer <= Zeitlimit:
                    Punktestand = Punktestand+1
                
                if Punktestand > 9:
                    Punktestand =0
                    Zehner=Zehner+1
                    Display.Show1(3, Punktestand)
                    Display.Show1(2, Zehner)
                Display.Show1(3,Punktestand)
                Display.Show1(2, Zehner)
    Startzeit = 0
    Zeitdauer = 0
    Punktestand = 0
    Zehner=0

# Bisher Probleme/ was fehlt: Das Programm funktioniert nur einmal, danach
# reagiert es auf den Startknopf nichtmehr.(gelöst!) EIn Highscore wird noch nicht gezählt,
# kein Buzzer drin, kein Led Ring oder 7-Segment-Anzeige. Die Buttons simulieren
# die Stationen und können u.U. später durch Funktionen, die man aufruft
# ersetzt werden(?)
