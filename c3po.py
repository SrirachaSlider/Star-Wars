#!/usr/bin/env python3
import os
import random
from gpiozero import LED, Button, DistanceSensor, Motor, Servo
from time import sleep

led = LED(22)
button = Button(18)

button.when_pressed = led.on
button.when_released = led.off

# Set the sensor to trigger at 0.305 meters (about 1 foot)
sensor = DistanceSensor(echo=24, trigger=23, threshold_distance=0.305)

def play_random_audio():
    voice_lines = ["C3PO.mp3", "Careful.mp3", "R2D2.mp3"]
    chosen_line = random.choice(voice_lines)
    os.system(f"mpg123 '{chosen_line}'")

# This runs the audio block in the background whenever someone gets close
sensor.when_in_range = play_random_audio

motor = Motor(forward=17, backward=27, enable=25)
actions = {'CW': motor.forward, 'CCW': motor.backward, 'STOP': motor.stop}

myCorrection = 0.45
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000
servo1 = Servo(12, min_pulse_width=minPW, max_pulse_width=maxPW)
servo2 = Servo(16, min_pulse_width=minPW, max_pulse_width=maxPW)

try:
    while True:
        dis = sensor.distance * 100
        print('Distance: {:.2f} cm'.format(dis))
        sleep(0.3)

        for action in ['CW', 'STOP', 'CCW', 'STOP']:
            actions[action]()
            print(f"{action}")
            sleep(5)

        servo1.mid()
        servo2.mid()
        print("mid")
        sleep(0.5)

        servo1.min()
        servo2.min()
        print("min")
        sleep(1)

        servo1.mid()
        servo2.mid()
        print("mid")
        sleep(0.5)

        servo1.max()
        servo2.max()
        print("max")
        sleep(1)

except KeyboardInterrupt:
    motor.stop()
    led.off()
    servo1.detach()
    servo2.detach()
    pass
