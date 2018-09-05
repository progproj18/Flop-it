
import RPi.GPIO as GPIO
import time
import random
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) #Pinnummern, alternativ GPIO.BCM für GPIO-Nummerierung
#Pins:
LedR = 40  #x=1 (21)<--in Klammern die GPIO-Pinnummern
LedG = 38  #x=2 (20)
LedB = 37  #x=3 (26)
LedY = 36  #x=4 (16)
LedW = 35  #(19) Led am Startbutton
Start_Button = 33 #(13)
Joystick = 32     #(12)    Die Buttons repräsentieren besagte Stationen
Lichtschranke = 31#(6) 
Keypad = 29       #(5) 
Kartenleser = 26  #(7) 
#Aus-/Eingänge:
GPIO.setup(LedR, GPIO.OUT)
GPIO.setup(LedG, GPIO.OUT)
GPIO.setup(LedB, GPIO.OUT)
GPIO.setup(LedY, GPIO.OUT)
GPIO.setup(LedW, GPIO.OUT)
GPIO.setup(Start_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #legt Ausgangszustand auf Low(0) fest
GPIO.setup(Joystick, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Keypad, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Lichtschranke, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Kartenleser, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.add_event_detect(Start_Button, GPIO.RISING,callback)<--ignorieren
#Variablen:
Startzeit = 0
Zeitlimit = 20
Zeitdauer = 0
#Funktionen

# Endlosschleife
while True:
    GPIO.output(LedW, GPIO.HIGH)
    GPIO.wait_for_edge(Start_Button, GPIO.RISING)
   #if GPIO.input(Start_Button) == 1:       
    GPIO.output(LedW, GPIO.LOW)# Ausschalten, optional: countdown+buzzer    
    #Zeit starten:
    Startzeit = time.clock()
    while Zeitdauer <= Zeitlimit:
        x = random.randint(1,4)
            
        if x == 1 :
            GPIO.output(LedR, GPIO.HIGH)
            while GPIO.input(Joystick) == 0:
                #Zeit messen:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedR, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                    
        elif x == 2 :
            GPIO.output(LedG, GPIO.HIGH)
            while GPIO.input(Lichtschranke) == 0:
                    Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedG, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                    
        elif x == 3 :
            GPIO.output(LedB, GPIO.HIGH)
            while GPIO.input(Keypad) == 0:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedB, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
                    
        elif x == 4 :
            GPIO.output(LedY, GPIO.HIGH)
            while GPIO.input(Kartenleser) == 0:
                Zeitdauer = (time.clock()-Startzeit)
            else:
                GPIO.output(LedY, GPIO.LOW)
                Zeitdauer = (time.clock()-Startzeit)
    Startzeit = 0
    Zeitdauer = 0
# Bisher Probleme/ was fehlt: Das Programm funktioniert nur einmal, danach
# reagiert es auf den Startknopf nichtmehr. EIn Highscore wird noch nicht gezählt,
# kein Buzzer drin, kein Led Ring oder 7-Segment-Anzeige. Die Buttons simulieren
# die Stationen und können u.U. später durch Funktionen, die man aufruft
# ersetzt werden(?)
