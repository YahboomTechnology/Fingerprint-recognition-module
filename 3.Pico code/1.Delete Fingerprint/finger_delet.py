from machine import Pin, UART
from as608 import as608
import time

uart = UART(0, 57600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

time.sleep(1)
#Initialize the fingerprint recognition module
fig=as608(uart)
print('Initialized successfully')
#Delete the fingerprint with ID 3
fig.deletfig(3)


