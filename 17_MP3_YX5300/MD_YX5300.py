from machine import UART
from time import sleep


class MD_YX5300:
    def __init__(self, UART_NUMBER=2):
        self.command=bytearray()
        self.command.append(0x7e)
        self.command.append(0xFF)
        self.command.append(0x06)
        self.command.append(0x00)
        self.command.append(0x00)
        self.command.append(0x00)
        self.command.append(0x00)
        self.command.append(0xEF)
       
        self.uart = UART(UART_NUMBER, 9600)
        # set volume to mid point (0=min 30=max)
        self.volume_level=15
        self.set_volume(self.volume_level)
        sleep(0.5)


    def play_next(self):
        self.command[3]=0x01
        self.uart.write(self.command)


    def play_previous(self):
        self.command[3]=0x02
        self.uart.write(self.command)
       
    def play_track(self,track_id):
        self.command[3]=0x03
        self.command[6]=track_id
        self.uart.write(self.command)


    def play(self):
        self.command[3]=0x03
        self.command[6]=1
        self.uart.write(self.command)


    def volume_up(self,step_count=1):
        if self.volume_level<=(30-step_count):
            self.volume_level=self.volume_level+step_count
        else:
            self.volume_level=30
        self.set_volume(self.volume_level)
   
    def volume_down(self,step_count=1):
        if self.volume_level>=step_count:
            self.volume_level=self.volume_level-step_count
        else:
            self.volume_level=0
        self.set_volume(self.volume_level)
       
    def set_volume(self,level):
        self.command[3]=0x06
        self.command[6]=level
        self.uart.write(self.command)
       
    def sleep_module(self):
        self.command[3]=0x0A
        self.uart.write(self.command)
       
    def wakeup_module(self):
        self.command[3]=0x0B
        self.uart.write(self.command)
       
    def reset_module(self):
        self.command[3]=0x0C
        self.uart.write(self.command)
       
    def pause(self):
        self.command[3]=0x0E
        self.uart.write(self.command)
       
    def resume(self):
        self.command[3]=0x0D
        self.uart.write(self.command)
       
    def stop(self):
        self.command[3]=0x16
        self.uart.write(self.command)
