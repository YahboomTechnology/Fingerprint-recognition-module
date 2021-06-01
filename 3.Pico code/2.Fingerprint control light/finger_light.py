from machine import Pin, UART, PWM
from as608 import as608
import time

uart = UART(0, 57600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

time.sleep(1)
#Initialize the fingerprint recognition module
fig=as608(uart)
print('Initialized successfully')
time.sleep(0.1)

#Set RGB pin to output mode
rgb_b = PWM(Pin(13))
rgb_r = PWM(Pin(12))
rgb_g = PWM(Pin(11))
#Set the RGB lamp pin to PWM frequency to 1000
rgb_b.freq(1000)
rgb_r.freq(1000)
rgb_g.freq(1000)
while True:
    #Start to recognize fingerprints and print the recognition results
    fingerval = fig.disfig()
    print(fingerval)
    if fingerval == 1:
        rgb_b.duty_u16(65535)
        rgb_r.duty_u16(65535)
        rgb_g.duty_u16(65535)
    else:
        rgb_b.duty_u16(0)
        rgb_r.duty_u16(0)
        rgb_g.duty_u16(0)
    #Wait for release your finger
    fig.waitfig()
    time.sleep(1)


