import ubluetooth
import urandom
from machine import Timer

class BLEUART:
    def __init__(self, name="ESP32-BLE"):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.bt_irq)
        
        self.tx = None
        self.rx = None
        self.conn_handle = None

        # UART Service UUID
        UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        # RX Characteristic (write)
        RX_UUID = ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
        # TX Characteristic (notify)
        TX_UUID = ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

        self.tx = (TX_UUID, ubluetooth.FLAG_NOTIFY)
        self.rx = (RX_UUID, ubluetooth.FLAG_WRITE)

        UART_SERVICE = (UART_UUID, (self.tx, self.rx))
        SERVICES = (UART_SERVICE, )

        ((self.tx_handle, self.rx_handle), ) = self.ble.gatts_register_services(SERVICES)
        self.ble.gap_advertise(100, adv_data=self._advertise(name))

    def _advertise(self, name):
        name_bytes = bytes(name, 'utf-8')
        adv_data = bytearray()
        adv_data += bytes((len(name_bytes) + 1, 0x09)) + name_bytes
        return adv_data

    def bt_irq(self, event, data):
        if event == 1:  # central connected
            self.conn_handle, _, _ = data
            print("Device connected")
        elif event == 2:  # central disconnected
            print("Device disconnected")
            self.conn_handle = None
            self.ble.gap_advertise(100, adv_data=self._advertise("ESP32-BLE"))
        elif event == 3:  # write to RX
            conn_handle, attr_handle = data
            msg = self.ble.gatts_read(self.rx_handle).decode('utf-8').strip()
            print("Received:", msg)

    def send(self, data):
        if self.conn_handle is not None:
            self.ble.gatts_notify(self.conn_handle, self.tx_handle, data)

ble_uart = BLEUART()

def send_random(t):
    num = str(urandom.getrandbits(8))  # מספר אקראי בין 0 ל-255
    print("Sending:", num)
    ble_uart.send(num)

# שליחה כל 5 שניות
timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback=send_random)

