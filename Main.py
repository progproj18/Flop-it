import RPi.GPIO as GPIO
import time
import timeit
import random
import tm1637
import math
import spidev
import os
import Reader


# Define sensor channels (3 to 7 are unused)
mcp3008_switch_channel = 7
mcp3008_x_voltage_channel = 6
mcp3008_y_voltage_channel = 5
 
# Define RGB channels
red_led = 31
green_led = 36
blue_led = 37

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
red_led = 31
green_led = 36
blue_led = 37
center_x_pos = 523
center_y_pos = 504
 
#GPIO.setmode(GPIO.BOARD)
GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)

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
                #ROW = [31, 33, 35, 37]
                #COL = [36, 38, 40]
                
                MATRIX = [[1,2,3],
                          [4,5,6],
                          [7,8,9],
                          ["*",0,"#"]]
                
                input_correct = False

                while not input_correct:
                    result = []
                    while len(result) < 4:
                        for j in range(3):
                            GPIO.output(COL[j], 0)

                            for i in range(4):
                                if GPIO.input(ROW[i]) == 0:
                                    time.sleep(0.02)
                                    result.extend([MATRIX[i][j]])
                                    print (result)
                                    while(GPIO.input(ROW[i]) == 0):
                                          time.sleep(0.02)

                            GPIO.output(COL[j], 1)
                    input_correct = (result == Code)

            # call function
            check_keypad()
            Display.Clear()
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
            import math
            import RPi.GPIO as GPIO
            import spidev
            import time
            import os
            import random

            # Open SPI bus
            spi = spidev.SpiDev()
            spi.open(0, 1)
            spi.max_speed_hz=1000
             
            # Define sensor channels (3 to 7 are unused)
            mcp3008_switch_channel = 7
            mcp3008_x_voltage_channel = 6
            mcp3008_y_voltage_channel = 5
             
            # Define RGB channels
            red_led = 31
            green_led = 36
            blue_led = 37

                
            def read_spi_data_channel(channel):
                
                """Read in SPI data from the channel and return a coordinate position
                :param channel: integer, between 0-7
                :return: integer, between 0-1023 indicating joystick position
                 """
             
                adc = spi.xfer2([1, (8+channel) << 4, 0])
                return ((adc[1] & 3) << 8) + adc[2]
             
             
            def convert_coordinates_to_angle(x, y, center_x_pos, center_y_pos):
                
                """
                Convert an x,y coordinate pair representing joystick position,
                and convert it to an angle relative to the joystick center (resting) position
                :param x: integer, between 0-1023 indicating position on x-axis
                :param y: integer, between 0-1023 indicating position on y-axis
                :param center_x_pos: integer, indicating resting position of joystick along x-axis
                :param center_y_pos: integer, indicating resting position of joystick along y-axis
                :return: integer, between 0-359 indicating angle in degrees
                """
                dx = x - center_x_pos
                dy = y - center_y_pos
                rads = math.atan2(-dy, dx)
                rads %= 2 * math.pi
                return math.degrees(rads)
             
             
            def adjust_angle_for_perspective_of_current_led(angle, led):
                """
                Take the current LED into account, and rotate the coordinate plane 360 deg to make PWM calculations easier
                :param angle: integer, between 0-359 indicating current angle of joystick position
                :param led: 'R', 'G', 'B', indicating the LED we're interested in
                :return: integer, between 0-359 indicating new angle relative to the current LED under consideration
                """
             
                led_peak_angle = 90 if led == 'R' else (210 if led == 'B' else 330)
                return ((angle - led_peak_angle) + 360) % 360
             
             
            def calculate_next_pwm_duty_cycle_for_led(angle, led):
                """
                Calculate the next PWM duty cycle value for the current LED and joystick position (angle)
                :param angle: integer, between 0-359 indicating current angle of joystick position
                :param led: 'R', 'G', 'B', indicating the LED we're interested in
                :return: integer, between 0-100 indicating the next PWM duty cycle value for the LED
                """
             
                angle = adjust_angle_for_perspective_of_current_led(angle, led)
                if 120 < angle < 240:
                    return 0
                elif angle <= 120:
                    return 100 - (angle * (100 / 120.0))
                else:
                    return 100 - ((360 - angle) * (100 / 120.0))
             
             
            def is_joystick_near_center(x, y, center_x_pos, center_y_pos):
                """
                Compare the current joystick position to resting position and decide if it's close enough to be considered "center"
                :param x: integer, between 0-1023 indicating position on x-axis
                :param y: integer, between 0-1023 indicating position on y-axis
                :param center_x_pos: integer, indicating resting position of joystick along x-axis
                :param center_y_pos: integer, indicating resting position of joystick along y-axis
                :return: boolean, indicating whether or not the joystick is near the center (resting) position
                """
             
                dx = math.fabs(x - center_x_pos)
                dy = math.fabs(y - center_y_pos)
                return dx < 20 and dy < 20
             


            """
            Initializes GPIO and PWM, then sets up a loop to continually read the joystick position and calculate the next set
            of PWM value for the RGB LED. When user hits ctrl^c, everything is cleaned up (see 'finally' block)
            :return: None
            """
             
            # Center positions when joystick is at rest
            center_x_pos = 523
            center_y_pos = 504
             
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)
             
            pwm_r = GPIO.PWM(red_led, 300)
            pwm_g = GPIO.PWM(green_led, 300)
            pwm_b = GPIO.PWM(blue_led, 300)

            pwm_instances = [pwm_r, pwm_g, pwm_b]
             
            for p in pwm_instances:
                p.start(0)
                    
            angle = 0
            x = 0
            try:
                for x in range(1):
                    Zufallswinkel = random.randint(0,359)
                    r = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'R')
                    g = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'G')
                    b = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'B')
                    
                    while angle < (Zufallswinkel-1) or angle > (Zufallswinkel+1):
                        # If joystick switch is pressed down, turn off LEDs
                        switch = read_spi_data_channel(mcp3008_switch_channel)
                            
                        if switch == 0:
                            for p in pwm_instances:
                                p.ChangeDutyCycle(0)
                            continue
             
                        # Read the joystick position data
                        x_pos = read_spi_data_channel(mcp3008_x_voltage_channel)
                        y_pos = read_spi_data_channel(mcp3008_y_voltage_channel)
             
                        # If joystick is at rest in center, turn on all LEDs at max
                        if is_joystick_near_center(x_pos, y_pos, center_x_pos, center_y_pos):
                            pwm_r.ChangeDutyCycle(r)
                            pwm_g.ChangeDutyCycle(g)
                            pwm_b.ChangeDutyCycle(b)
                            #for p in pwm_instances:
                                #p.ChangeDutyCycle(100)
                            continue
                        
                        # Adjust duty cycle of LEDs based on joystick position
                        angle = convert_coordinates_to_angle(x_pos, y_pos, center_x_pos, center_y_pos)
                        pwm_r.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'R'))
                        pwm_g.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'G'))
                        pwm_b.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'B'))
             
                        #print("Position : ({},{})  --  Angle : {}".format(x_pos, y_pos, round(angle, 2)))
                    for p in pwm_instances:
                        p.ChangeDutyCycle(0)
                    print ("Korrekt!")
                    x = x+1
                    time.sleep(0.5)

            except KeyboardInterrupt:
                pass
            finally:
                p.stop()
                spi.close()
  
                        
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

