from machine import Pin, UART
from as608 import as608
import time

uart = UART(0, 57600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

time.sleep(1)
#Initialize the fingerprint recognition module
fig=as608(uart)
print('Initialized successfully')
time.sleep(0.1)
while True:
    #Start to recognize fingerprints and print the recognition results
    print(fig.disfig())
    #Wait for your finger to release
    fig.waitfig()
    time.sleep(1)


