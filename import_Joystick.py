import RPi.GPIO as GPIO
import timeit
#import random

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD) 
#while True:
if __name__ == "__main__":
    Startzeit = timeit.default_timer()
    print (Startzeit)
    import Joystick_Funktion
#Colour = Joystick_Funktion.RGB #2 entspricht helligkeit
    Zeitdauer = (timeit.default_timer()-Startzeit)

    print (Zeitdauer)
 