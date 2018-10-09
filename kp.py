# Quelle: https://www.youtube.com/watch?v=yYnX5QodqQ4
# ab hier Zitat, auskommentierte Prints wurden nicht extra markiert
#---------------------------------------------------------------------------------------------------------------------------
import RPi.GPIO as GPIO
import time
import random
import tm1637

#GPIO Setup
GPIO.setmode (GPIO.BOARD)
GPIO.setwarnings(False)

#Display Setup
Display = tm1637.TM1637(3,5,2)
Display.Clear()
#---------------------------------------------------------------------------------------------------------------------------
def kp():                                        # eine Funktion um alles herum, die nur aufgerufen werden muss
#---------------------------------------------------------------------------------------------------------------------------
    Code = []
    for _ in range(4):
        Code.append(random.randint(0, 9))
       
    #Show Code
    #for _ in range (1):
    Display.Show(Code)

    #Password From KeyPad
    print("Please Enter User Password: ")

    #Keypad Setup
    ROW = [7,11,13,15]
    COL = [12,16,18]

    for j in range(3):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)
    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)


    def check_keypad():
    
        MATRIX = [[1,2,3],
                  [4,5,6],
                  [7,8,9],
                  ["*",0,"#"]]
 #---------------------------------------------------------------------------------------------------------------------------       
        input_correct = False

        while not input_correct:                                                          #Schleife läuft, solange die Eingabe falsch ist
            result = []
            while len(result) < 4:                                                        #Eingaben werden in Liste result zugefügt, bis sie die Länge 4 hat
                for j in range(3):
                    GPIO.output(COL[j], 0)

                    for i in range(4):
                        if GPIO.input(ROW[i]) == 0:
                            time.sleep(0.02)
                            result.extend([MATRIX[i][j]])                                  #über .extend Befehl wird in die Liste result geschrieben
                            print (result)
                            while(GPIO.input(ROW[i]) == 0):
                                  time.sleep(0.02)                                         #verhindert dass die gleich Zahl mehrfach ausgegeben wird

                    GPIO.output(COL[j], 1)
            input_correct = (result == Code)                                               #while not Schleife wird unterbrochen, wenn die Eingabe dem generiertem Code entspricht

    # call function
    check_keypad()
    Display.Clear()
#kp()
#
