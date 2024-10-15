from machine import UART
import utime




uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
print(uart)




print("---------------------------------------------------------------------")
print("|  Module HC-06 configuration                                       |")
print("|  enter AT              -- To test serial communication            |")
print("|  enter AT+NAME??????   -- To modify the module name               |")
print("|  enter AT+PIN1234      -- To modify the module PIN code           |")
print("|  enter AT+BAUD4        -- To modify the module communication speed|")
print("|  Note: 1 for 1200,  2 for 2400,  3 for 4800,  4 for 9600          |")
print("|        5 for 19200, 6 for 38400, 7 for 57600, 8 for 115200        |")
print("---------------------------------------------------------------------")




while True:
    print("ENTER AT Commands: ")
    try:
        str = input()
        uart.write(str)
        utime.sleep_ms(100)
    except OSError:
        pass




    # wait for response    
    start_time = utime.ticks_ms()
    timeout = False
    while not uart.any() and not timeout:
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 500:
            timeout = True
    if timeout:
        print('Failed, response timed out')
    else:
        buf = uart.read()
        print("received:",buf)
    utime.sleep_ms(600)
