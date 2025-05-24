import ubluetooth
import utime
import urandom
from machine import Timer

ble = ubluetooth.BLE()
ble.active(True)

#Personal UUID generator https://www.uuidgenerator.net
UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID = ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID = ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

UART_SERVICE = (
    UART_UUID,
    (
        (TX_UUID, ubluetooth.FLAG_NOTIFY),
        (RX_UUID, ubluetooth.FLAG_WRITE),
    ),
)

handles = ble.gatts_register_services((UART_SERVICE,))
tx_handle = handles[0][0]
rx_handle = handles[0][1]
conn_handle = None

def advertise():
    name = b'ESP32-BLE'
    adv_data = bytearray()
    adv_data += bytes((len(name) + 1, 0x09)) + name
    ble.gap_advertise(100, adv_data)

def bt_irq(event, data):
    global conn_handle
    if event == 1:
        conn_handle = data[0]
        print("Connected")
    elif event == 2:
        print("Disconnected")
        conn_handle = None
        advertise()
    elif event == 3:
        msg = ble.gatts_read(rx_handle).decode('utf-8').strip()
        print("Received:", msg)

ble.irq(bt_irq)
advertise()

def send_random(timer):
    if conn_handle is not None:
        value = str(urandom.getrandbits(8))
        print("Sending:", value)
        ble.gatts_notify(conn_handle, tx_handle, value)
      

timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback=send_random)
print("Waiting to connect...")
