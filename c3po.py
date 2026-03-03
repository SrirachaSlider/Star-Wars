#!/usr/bin/env python3
from gpiozero import LED, Button, DistanceSensor, Motor, Servo, Buzzer
from time import sleep

led = LED(22)
button = Button(18)

button.when_pressed = led.on
button.when_released = led.off

sensor = DistanceSensor(echo=24, trigger=23, threshold_distance=0.305)
buzzer = Buzzer(21)

def sound_buzzer():
    for _ in range(3):
        print('Buzzer On')
        buzzer.on()
        sleep(0.1)
        print('Buzzer Off')
        buzzer.off()
        sleep(0.1)

sensor.when_in_range = sound_buzzer

motor = Motor(forward=19, backward=22, enable=4)
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
