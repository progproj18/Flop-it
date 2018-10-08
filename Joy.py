# Quelle: https://grantwinney.com/connecting-an-analog-joystick-to-the-raspberry-pi-and-using-it-with-an-rgb-led-to-simulate-a-color-wheel/

# ab hier Zitat, auskommentierte Prints wurden nicht extra markiert, anders belegte Pinnumern ebenfalls nicht

#---------------------------------------------------------------------------------------------------------------------------
import math
import RPi.GPIO as GPIO
import spidev
import time
import os
import random
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz=100
             
# Define sensor channels (3 to 7 are unused)
mcp3008_switch_channel = 7
mcp3008_x_voltage_channel = 6
mcp3008_y_voltage_channel = 5

center_x_pos = 523
center_y_pos = 504
# Define RGB channels
red_led = 31
green_led = 36
blue_led = 37
#GPIO.setmode(GPIO.BOARD)
GPIO.setup([red_led, green_led, blue_led], GPIO.OUT, initial=GPIO.LOW)
pwm_r = GPIO.PWM(red_led, 300)
pwm_g = GPIO.PWM(green_led, 300)
pwm_b = GPIO.PWM(blue_led, 300)
                
#---------------------------------------------------------------------------------------------------------------------------
def Joys():    # allumfassende Funktion
#---------------------------------------------------------------------------------------------------------------------------    
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
#---------------------------------------------------------------------------------------------------------------------------
        return dx < 35 and dy < 35                      # der Toleranzbereich musste vergroeßert werden (von 20--> 35), gegen Flackern der LED
#---------------------------------------------------------------------------------------------------------------------------

    """
    Initializes GPIO and PWM, then sets up a loop to continually read the joystick position and calculate the next set
    of PWM value for the RGB LED. When user hits ctrl^c, everything is cleaned up (see 'finally' block)
    :return: None
    """
             

    pwm_instances = [pwm_r, pwm_g, pwm_b]
             
    for p in pwm_instances:
        p.start(0)
#---------------------------------------------------------------------------------------------------------------------------
    angle = 0
    x = 0
    try:
        for x in range(1):                                       # fuer den Fall, dass mehrere Durchlauufe erwuenscht sind
            Zufallswinkel = random.randint(0,359)                # Bestimmung Zufallswinkel + entsprechende Farbe der Led
            r = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'R')
            g = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'G')
            b = calculate_next_pwm_duty_cycle_for_led(Zufallswinkel, 'B')
                    
            while angle < (Zufallswinkel-1) or angle > (Zufallswinkel+1):   # Auslesen des Joysticks und Pruefen auf Position (bzgl. Zufallswinkels)
                                                                            # mit 1° Toleranz
 #---------------------------------------------------------------------------------------------------------------------------
                switch = read_spi_data_channel(mcp3008_switch_channel)
                            
                if switch == 0:                                             # switch gedrueckt --> Led aus
                    for p in pwm_instances:
                        p.ChangeDutyCycle(0)
                    continue
#---------------------------------------------------------------------------------------------------------------------------             
                x_pos = read_spi_data_channel(mcp3008_x_voltage_channel)    # Joystick auslesen, x-/y-Position
                y_pos = read_spi_data_channel(mcp3008_y_voltage_channel)
             
                if is_joystick_near_center(x_pos, y_pos, center_x_pos, center_y_pos):  # Wenn Joystick in Ruhelage, LED leuchtet in Zufallsfarbe
                    pwm_r.ChangeDutyCycle(r)
                    pwm_g.ChangeDutyCycle(g)
                    pwm_b.ChangeDutyCycle(b)
                    continue
                        
                angle = convert_coordinates_to_angle(x_pos, y_pos, center_x_pos, center_y_pos)  # Umsetzen der Joystickposition in Led-Farbe
                pwm_r.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'R'))
                pwm_g.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'G'))
                pwm_b.ChangeDutyCycle(calculate_next_pwm_duty_cycle_for_led(angle, 'B'))

            for p in pwm_instances:
                p.ChangeDutyCycle(0)                   # Led aus
            print ("Korrekt!")
            x = x+1
            time.sleep(0.5)
#---------------------------------------------------------------------------------------------------------------------------
    except KeyboardInterrupt:
        pass
