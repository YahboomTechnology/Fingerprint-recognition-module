# -*- coding:utf-8 -*-
import binascii
import serial
import time
#Configure the serial port
ser = serial.Serial("/dev/ttyAMA0", 57600)

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
    hc = str(binascii.b2a_hex(hc))[23:24]
    while hc!='a':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[23:24]
        ser.flushInput()

def disfig():
    print('Press your finger')
    searchfig()
    print('Identifying')
    time.sleep(0.02)
    sendcmd(cmd_gen1)
    time.sleep(0.01)
    ser.flushInput()
    time.sleep(0.01)
    sendcmd(cmd_dis)
    time.sleep(0.01)
    count = ser.inWaiting()
    hc = ser.read(count)
    disno = str(binascii.b2a_hex(hc))[19:20]
    disid =  str(binascii.b2a_hex(hc))[23:24]
    #print(disno)
    #print(disid)
    print("Recognition result:")
    time.sleep(0.01)
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
    hc = str(binascii.b2a_hex(hc))[23:24]
    print('Release your finger')
    while hc=='a':
        time.sleep(0.1)
        sendcmd(cmd_search)
        time.sleep(0.1)
        count = ser.inWaiting()
        hc = ser.read(count)
        hc = str(binascii.b2a_hex(hc))[23:24]
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
    reg = str(binascii.b2a_hex(reg))[18:19]
    #print(reg)
    if reg=='0':
        add=cmd_save+bytearray([addr,0,addr+0xe])
        sendcmd(add)
        print('Deposit successfully')
    else :
        print('Deposit failed')
    ser.flushInput()

def deletfig(addr):
    deletchar=cmd_deletchar+bytearray([addr,0,1,0,addr+0x15])
    sendcmd(deletchar)
    time.sleep(0.5)
    count = ser.inWaiting()
    reg = ser.read(count)
    ser.flushInput()
    print('The delete command is executed')

time.sleep(1)
#Initialize the fingerprint recognition module
init()
print('初始化成功')
time.sleep(0.1)
#Delete the fingerprint with ID 3
deletfig(3)
