from machine import UART
import time

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

class as608:
    def __init__(self,uart):
        self.uart = uart
        self.sendcmd(link)
        self.sendcmd(readflash)
        self.sendcmd(readmould)
        self.sendcmd(readindex)
        self.sendcmd(readindex1)
        time.sleep(0.01)
        a=0#Clear
        while self.uart.read(1)!=b'\n':
            a+=1
            if a > 11:
                print("Initialization failed, please check the wiring and run again")

    def sendcmd(self,cmd):
        self.uart.write(head)
        self.uart.write(cmd)

    def searchfig(self):
        hc={0}
        self.sendcmd(cmd_search)
        hc=self.uart.read(12)
        while hc[11]!=0xa:
            if hc[11] != 0xa and hc[11] != 0xc:
                self.uart.read(4)
                #print('1')
            self.sendcmd(cmd_search)
            hc=self.uart.read(12)
            #print(hc)
            time.sleep(0.01)

    def waitfig(self):
        hc={0}
        self.sendcmd(cmd_search)
        hc=self.uart.read(12)
        print('Release your finger')
        while hc[11]==0xa:
            self.sendcmd(cmd_search)
            hc=self.uart.read(12)
            time.sleep(0.01)

    def disfig(self):
        print('Press your finger')
        self.searchfig()
        print('Identifying')
        time.sleep(0.02)
        self.sendcmd(cmd_gen1)
        self.sendcmd(cmd_dis)
        time.sleep(0.01)
        hc=self.uart.read(16)
        #print(hc)
        print("Recognition result:")
        time.sleep(0.01)
        if hc[9]==9:
            return "No matching fingerprint found"
        else :
            return hc[11]

    def savefig(self,addr):
        reg={0}
        print('Press your finger')
        self.searchfig()
        self.sendcmd(cmd_gen1)
        print('Press your finger again')
        time.sleep(3)
        self.searchfig()
        self.sendcmd(cmd_gen2)
        self.sendcmd(cmd_reg)
        self.sendcmd(cmd_reg)
        time.sleep(0.1)
        reg=self.uart.read(12)
        #print(reg)
        if reg[9]==0:
            add=cmd_save+bytearray([addr,0,addr+0xe])
            self.sendcmd(add)
            print('Deposited successfully')
        else :
            print('Deposit successfully')

    def deletfig(self,addr):
        de={0}
        deletchar=cmd_deletchar+bytearray([addr,0,1,0,addr+0x15])
        self.sendcmd(deletchar)
        time.sleep(0.5)
        self.uart.read(12)
        print('Delete command is executed')

