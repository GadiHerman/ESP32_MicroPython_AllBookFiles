from machine import UART
import MD_YX5300

uart = UART(1, baudrate=9600, tx=19, rx=18)
#uart = UART(2, 9600)
mp3 = MD_YX5300.MD_YX5300(uart)
mp3.play_track(1)