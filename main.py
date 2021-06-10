#Guilherme Souza
#Creative Commons Attribution, Share-alike 4.0 (CC BY-SA 4.0)

#This is micropython code for using a rotary encoder to control each
#color. Rotate to change the component of red, and then click to change
#which color component you are setting.

#for hookup diagrams see:
#https://github.com/guilerms/RGB_led_controlled_by_rotary_encoder

#Huge thanks to Mike Teachman for his brilliant library for using rotary
#encoders with micropython.
#https://github.com/MikeTeachman/micropython-rotary

#importing relevant libraries
import time
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin, PWM

#pin settings
button = Pin(18, Pin.IN, Pin.PULL_DOWN)

rPin = PWM(Pin(0))
gPin = PWM(Pin(2))
bPin = PWM(Pin(3))

rPin.freq(1000)
gPin.freq(1000)
bPin.freq(1000)

#constructing the encoder instance
e = RotaryIRQ(pin_num_clk=16,
              pin_num_dt=17,
              min_val=0,
              max_val=19,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

colors = ("red", "green", "blue") #this is only for debugging

currentColor = 0

#these variables hold the current values for each color, in 0-19 range
rVal = 0
gVal = 0
bVal = 0

valOld = e.value()

def updateLed():
        #here we update the RGB LED output pins with the correct PWM
        #duty cycle. the calculation is necessary to put each color
        #from a 20 steps range (full rotation of the rotary encoder)
        #to the PWM range. each color, though, has a different max
        #value, determined experimentally. the red part on the RGB
        #LED is much brighter, thus it accepts a lower max value.
        #blue is the faintest, so it gets the whole PWM range.
        rPin.duty_u16(int(rVal*25000/19))
        gPin.duty_u16(int(gVal*40000/19))
        bPin.duty_u16(int(bVal*65025/19))

def changeColor(pin):
    #this is for iterating which color we are setting with the encoder
    global currentColor
    if currentColor < 2:
        currentColor = currentColor + 1
    else:
        currentColor = 0
    if currentColor == 0:
        e.set(value = rVal)
    if currentColor == 1:
        e.set(value = gVal)
    if currentColor == 2:
        e.set(value = bVal)
    print('current color =', colors[currentColor])

button.irq(trigger = Pin.IRQ_FALLING, handler = changeColor)

while True:
    #print("e.value = ", e.value())

    if currentColor == 0:
        rVal = valNew = e.value()
    if currentColor == 1:
        gVal = valNew = e.value()
    if currentColor == 2:
        bVal = valNew = e.value()

    if valOld != valNew:
        valOld = valNew

    updateLed()

    #10 ms delay
    time.sleep_ms(10)
