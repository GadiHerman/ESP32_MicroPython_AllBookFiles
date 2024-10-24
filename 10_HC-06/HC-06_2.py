from machine import UART
import utime

"""
ESP32 UART2           HC-06 / CH-05 
GPIO_17_UART2_TX           RX
GPIO_16_UART2_RX           TX

To enter AT-Command mode in HC05:
Press & Hold the onboard button while power on.

To enter AT-Command mode in HC06:
Power-up in NOT CONNECTED

Baudrate for at-comand mode in HC05: 38400
Baudrate for at-comand mode in HC06: 9600

"""
NAME = "HC05_MGK3"
PASSWORD = "1234"
uart2 = UART(2,baudrate=38400)    # at-comand baudrate for HC05
# uart2 = UART(2,baudrate=9600)   # at-comand baudrate for HC06 
print(uart2)

#2 sec timeout is arbitrarily chosen
def sendAT(cmd, uart=uart2, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    
def waitResp(uart=uart2, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
        decoded_string = resp.decode("utf-8")
    print(decoded_string)

#commands for HC-06 version:   VERSION:3.0-20170609
#commands for HC-05 version:   VERSION:2.0-20100601
print("---- Start ----")
waitResp()
sendAT("AT\r\n")
sendAT("AT+ORGL\r\n")           #Restore default setting
sendAT("AT+VERSION\r\n")
sendAT("AT+UART?\r\n")
sendAT("AT+UART=9600,0,0\r\n")  #9600 baud, 1 stop, parity=none
sendAT("AT+UART?\r\n")
sendAT("AT+PSWD?\r\n")
sendAT("AT+PSWD=\""+PASSWORD+"\"\r\n") 
sendAT("AT+PSWD?\r\n")
sendAT("AT+NAME=\""+NAME+"\"\r\n")
sendAT("AT+NAME?\r\n")
sendAT("AT+ADDR?\r\n")
print("---- Done ----")

#commands for HC-06 version:   hc01.comV2.0  ,  linvorV1.8
# print("---- Start ----")
# waitResp()
# sendAT("AT")
# sendAT("AT+VERSION")
# sendAT("AT+BAUD4")            #4 ——> 9600
# sendAT("AT+NAME"+NAME)
# sendAT("AT+PIN"+PASSWORD)
# sendAT("AT+PN")               #AT+PN sets no parity
# print("---- Done ----")
