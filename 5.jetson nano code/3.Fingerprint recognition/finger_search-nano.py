# -*- coding:utf-8 -*-
import binascii
import serial
import time
#Configure the serial port
ser = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=57600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

head=b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00'
link=b'\x07\x13\x00\x00\x00\x00\x00\x1B'
readflash=b'\x03\x16\x00\x1A'
readmould=b'\x03\x1D\x00\x21'
readindex=b'\x04\x1F\x00\x00\x24'
readindex1=b'\x04\x1F\x01\x00\x25'
cmd_search=b'\x03\x01\x00\x05'
cmd_upload=b'\x03\x0A\x00\x0E'
cmd_gen1=b'\x04\x02\x01\x00\x08'
cmd_gen2=b'\x04\x02\x02\x00\x09'
cmd_reg=b'\x03\x05\x00\x09'
cmd_save=b'\x06\x06\x01\x00'
cmd_dis=b'\x08\x04\x01\x00\x00\x01\x2C\x00\x3B'
cmd_deletchar=b'\x07\x0c\x00'


def sendcmd(cmd):
    ser.write(head)
    ser.write(cmd)
    time.sleep(0.35)
    
def init():
    sendcmd(link)
    sendcmd(readflash)
    sendcmd(readmould)
    sendcmd(readindex)
    ser.flushInput()
    sendcmd(readindex1)
    count = ser.inWaiting()
    recv = ser.read(count)
    recv = str(binascii.b2a_hex(recv))[0:44]
    #print(count)
    #print(recv)
    ser.flushInput()

def searchfig():
    time.sleep(0.1)
    sendcmd(cmd_search)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    hc = str(binascii.b2a_hex(hc))[21:22]
    while hc=='2':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        ser.flushInput()
        time.sleep(0.5)

def disfig():
    print('Press your finger')
    searchfig()
    print('Identifying')
    time.sleep(0.2)
    sendcmd(cmd_gen1)
    time.sleep(0.1)
    ser.flushInput()
    time.sleep(0.1)
    sendcmd(cmd_dis)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    #print(hc)
    disno = str(binascii.b2a_hex(hc))[21:22]
    disid =  str(binascii.b2a_hex(hc))[25:26]
    #print(disno)
    #print(disid)
    print("Recognition result:")
    time.sleep(0.1)
    if disno=='9':
        return "No matching fingerprint found"
    else :
        return disid

def waitfig():
    time.sleep(0.1)
    sendcmd(cmd_search)
    time.sleep(0.1)
    count = ser.inWaiting()
    hc = ser.read(count)
    hc = str(binascii.b2a_hex(hc))[21:22]
    print('Release your finger')
    while hc=='0':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[21:22]
        ser.flushInput()

def savefig(addr):
    print('Press your finger')
    searchfig()
    sendcmd(cmd_gen1)
    print('Press your finger again')
    time.sleep(3)
    searchfig()
    sendcmd(cmd_gen2)
    time.sleep(0.1)
    ser.flushInput()
    sendcmd(cmd_reg)
    time.sleep(0.1)
    count = ser.inWaiting()
    reg = ser.read(count)
    reg = str(binascii.b2a_hex(reg))[20:21]
    #print(reg)
    if reg=='0':
        add=cmd_save+bytearray([addr,0,addr+0xe])
        sendcmd(add)
        print('Deposited successfully')
    else :
        print('Deposited failed')
    ser.flushInput()

def deletfig(addr):
    deletchar=cmd_deletchar+bytearray([addr,0,1,0,addr+0x15])
    sendcmd(deletchar)
    time.sleep(0.5)
    count = ser.inWaiting()
    reg = ser.read(count)
    ser.flushInput()

time.sleep(1)
#Initialize the fingerprint recognition module
init()
print('Initialized successful')
time.sleep(0.1)
try:
    while True:
        #Start to recognize fingerprints and print the recognition results
        print(disfig())
        #Wait for your finger to release
        waitfig()
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting Program")

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))
finally:
    ser.close()
    pass
