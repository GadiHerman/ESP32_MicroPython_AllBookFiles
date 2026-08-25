from machine import Pin, I2C
import time


class Si4703Error(Exception):
    """Base exception for Si4703 errors."""
    pass


class Si4703TimeoutError(Si4703Error):
    """Raised when the Si4703 does not complete an operation in time."""
    pass


class Si4703CommunicationError(Si4703Error):
    """Raised when I2C communication fails."""
    pass


class Si4703:

    ADDRESS = 0x10

    REG_DEVICEID = 0x00
    REG_CHIPID = 0x01
    REG_POWERCFG = 0x02
    REG_CHANNEL = 0x03
    REG_SYSCONFIG1 = 0x04
    REG_SYSCONFIG2 = 0x05
    REG_SYSCONFIG3 = 0x06
    REG_STATUSRSSI = 0x0A
    REG_READCHAN = 0x0B
    REG_TEST1 = 0x07

    POWERCFG_SMUTE = 15
    POWERCFG_DMUTE = 14
    POWERCFG_MONO = 13
    POWERCFG_SKMODE = 10
    POWERCFG_SEEKUP = 9
    POWERCFG_SEEK = 8
    POWERCFG_DISABLE = 6
    POWERCFG_ENABLE = 0

    CHANNEL_TUNE = 15

    SYSCONFIG1_RDS = 12
    SYSCONFIG1_DE = 11

    SYSCONFIG2_SPACE1 = 5
    SYSCONFIG2_SPACE0 = 4
    SYSCONFIG2_VOLUME_MASK = 0x000F

    STATUS_STC = 14
    STATUS_SFBL = 13
    STATUS_AFCRL = 12
    STATUS_STEREO = 8
    STATUS_RSSI_MASK = 0x00FF

    def __init__(
        self,
        i2c,
        reset_pin,
        sen_pin
    ):
        self.i2c = i2c
        self.reset_pin = reset_pin
        self.sen_pin = sen_pin

        self.registers = [0] * 16

        self.initialized = False

    def _read_all_registers(self):
        # The Si4703 starts reading at register 0x0A.
        # It continues through 0x0F and then wraps to 0x00.

        try:
            data = self.i2c.readfrom(self.ADDRESS, 32)
        except OSError as error:
            raise Si4703CommunicationError(
                "I2C read failed: {}".format(error)
            )

        if len(data) != 32:
            raise Si4703CommunicationError(
                "Unexpected I2C data length"
            )

        register_number = 0x0A

        for index in range(0, 32, 2):

            high_byte = data[index]
            low_byte = data[index + 1]

            value = (high_byte << 8) | low_byte

            self.registers[register_number] = value

            register_number += 1

            if register_number == 0x10:
                register_number = 0

        return self.registers

    def _write_control_registers(self):
        # The Si4703 expects continuous writes starting at register 0x02.
        # Registers 0x02 through 0x07 are written here.

        data = bytearray()

        for register_number in range(0x02, 0x08):

            value = self.registers[register_number]

            high_byte = (value >> 8) & 0xFF
            low_byte = value & 0xFF

            data.append(high_byte)
            data.append(low_byte)

        try:
            self.i2c.writeto(self.ADDRESS, data)
        except OSError as error:
            raise Si4703CommunicationError(
                "I2C write failed: {}".format(error)
            )

    def reset(self):
        # Keep SEN high so that the Si4703 selects I2C mode.
        self.sen_pin.value(1)

        # Put the Si4703 into reset.
        self.reset_pin.value(0)

        time.sleep_ms(10)

        # Release reset.
        self.reset_pin.value(1)

        time.sleep_ms(10)

    def initialize(self):
        self.reset()

        # Check that the device responds before continuing.
        devices = self.i2c.scan()

        if self.ADDRESS not in devices:
            raise Si4703CommunicationError(
                "Si4703 was not found on the I2C bus"
            )

        self._read_all_registers()

        device_id = self.registers[self.REG_DEVICEID]
        chip_id = self.registers[self.REG_CHIPID]

        print("Device ID: 0x{:04X}".format(device_id))
        print("Chip ID: 0x{:04X}".format(chip_id))

        # Enable the internal oscillator.
        # The Si4703 needs the oscillator before tuning can work.
        self.registers[self.REG_TEST1] = 0x8100

        self._write_control_registers()

        # Wait for the oscillator to stabilize.
        time.sleep_ms(500)

        # Read the registers again after oscillator startup.
        self._read_all_registers()

        # Configure power.
        # DMUTE = 1
        # ENABLE = 1
        powercfg = self.registers[self.REG_POWERCFG]

        powercfg |= (1 << self.POWERCFG_DMUTE)
        powercfg |= (1 << self.POWERCFG_ENABLE)

        self.registers[self.REG_POWERCFG] = powercfg

        # Configure European-style 100 kHz channel spacing.
        #
        # SPACE = 01 means 100 kHz.
        sysconfig2 = self.registers[self.REG_SYSCONFIG2]

        sysconfig2 &= ~(1 << self.SYSCONFIG2_SPACE1)
        sysconfig2 |= (1 << self.SYSCONFIG2_SPACE0)

        # Start with a low volume.
        sysconfig2 &= ~self.SYSCONFIG2_VOLUME_MASK
        sysconfig2 |= 1

        self.registers[self.REG_SYSCONFIG2] = sysconfig2

        # Use 50 us de-emphasis.
        #
        # This setting is commonly used for Europe.
        sysconfig1 = self.registers[self.REG_SYSCONFIG1]

        sysconfig1 |= (1 << self.SYSCONFIG1_DE)

        self.registers[self.REG_SYSCONFIG1] = sysconfig1

        self._write_control_registers()

        # Wait for the power-up sequence to complete.
        time.sleep_ms(120)

        # Read the registers again so that the local shadow registers
        # contain the current device state.
        self._read_all_registers()

        self.initialized = True
    def _check_initialized(self):
        if not self.initialized:
            raise Si4703Error(
                "Si4703 has not been initialized"
            )

    def set_volume(self, volume):
        self._check_initialized()

        if not isinstance(volume, int):
            raise ValueError(
                "Volume must be an integer"
            )

        if volume < 0 or volume > 15:
            raise ValueError(
                "Volume must be between 0 and 15"
            )

        self._read_all_registers()

        value = self.registers[self.REG_SYSCONFIG2]

        value &= ~self.SYSCONFIG2_VOLUME_MASK
        value |= volume

        self.registers[self.REG_SYSCONFIG2] = value

        self._write_control_registers()

    def set_frequency(self, frequency_mhz):
        self._check_initialized()

        if not isinstance(frequency_mhz, (int, float)):
            raise ValueError(
                "Frequency must be a number"
            )

        if frequency_mhz < 87.5 or frequency_mhz > 108.0:
            raise ValueError(
                "Frequency must be between 87.5 and 108.0 MHz"
            )

        # For 100 kHz spacing and a 87.5 MHz band bottom:
        #
        # channel = (frequency - 87.5) / 0.1
        #
        # Example:
        # 100.3 MHz -> channel 128

        channel = int(round(
            (frequency_mhz - 87.5) / 0.1
        ))

        if channel < 0 or channel > 1023:
            raise ValueError(
                "Calculated channel is outside the valid range"
            )

        self._read_all_registers()

        # Preserve all other bits in CHANNEL.
        channel_register = self.registers[self.REG_CHANNEL]
        # Register 03 bit 15       = TUNE
        # Register 03 bits 14:10   = Reserved
        # Register 03 bits 9:0     = CHAN
        #old         channel_register &= 0xFC00
        channel_register &= 0x0400
        channel_register |= channel

        # Set TUNE.
        channel_register |= (1 << self.CHANNEL_TUNE)

        self.registers[self.REG_CHANNEL] = channel_register

        # self._write_control_registers()

        # # Wait for STC.
        # self._wait_for_stc()

        self._write_control_registers()

        print("TUNE command sent.")

        time.sleep_ms(100)

        self._read_all_registers()

        print(
            "POWERCFG: 0x{:04X}".format(
                self.registers[self.REG_POWERCFG]
            )
        )

        print(
            "CHANNEL: 0x{:04X}".format(
                self.registers[self.REG_CHANNEL]
            )
        )

        print(
            "STATUSRSSI: 0x{:04X}".format(
                self.registers[self.REG_STATUSRSSI]
            )
        )





        # Clear TUNE.
        self._read_all_registers()

        channel_register = self.registers[self.REG_CHANNEL]

        channel_register &= ~(1 << self.CHANNEL_TUNE)

        self.registers[self.REG_CHANNEL] = channel_register

        self._write_control_registers()

        # Read again after completing the tune operation.
        self._read_all_registers()

    def _wait_for_stc(self, timeout_ms=2000):
        start = time.ticks_ms()

        while True:

            self._read_all_registers()

            status = self.registers[self.REG_STATUSRSSI]

            stc = (
                status >> self.STATUS_STC
            ) & 1

            if stc:
                return

            elapsed = time.ticks_diff(
                time.ticks_ms(),
                start
            )

            if elapsed >= timeout_ms:
                raise Si4703TimeoutError(
                    "Timeout while waiting for STC"
                )

            # Keep this delay relatively large.
            # It also reduces unnecessary I2C traffic.
            time.sleep_ms(20)

    def _finish_seek(self):
        # The SEEK bit must be cleared after STC becomes active.

        self._read_all_registers()

        powercfg = self.registers[self.REG_POWERCFG]

        powercfg &= ~(1 << self.POWERCFG_SEEK)

        self.registers[self.REG_POWERCFG] = powercfg

        self._write_control_registers()

        time.sleep_ms(10)

        self._read_all_registers()

    def seek_up(self):
        self._check_initialized()

        self._read_all_registers()

        powercfg = self.registers[self.REG_POWERCFG]

        # SKMODE = 0 means that the tuner wraps around
        # when it reaches a band edge.
        powercfg &= ~(1 << self.POWERCFG_SKMODE)

        # SEEKUP = 1
        powercfg |= (1 << self.POWERCFG_SEEKUP)

        # SEEK = 1
        powercfg |= (1 << self.POWERCFG_SEEK)

        self.registers[self.REG_POWERCFG] = powercfg

        self._write_control_registers()

        self._wait_for_stc()

        self._finish_seek()

        status = self.registers[self.REG_STATUSRSSI]

        sfbl = (
            status >> self.STATUS_SFBL
        ) & 1

        if sfbl:
            raise Si4703Error(
                "Seek reached the band limit without finding a station"
            )

        return self.get_frequency()

    def seek_down(self):
        self._check_initialized()

        self._read_all_registers()

        powercfg = self.registers[self.REG_POWERCFG]

        # SKMODE = 0 means that the tuner wraps around
        # when it reaches a band edge.
        powercfg &= ~(1 << self.POWERCFG_SKMODE)

        # SEEKUP = 0 means seek downward.
        powercfg &= ~(1 << self.POWERCFG_SEEKUP)

        # SEEK = 1
        powercfg |= (1 << self.POWERCFG_SEEK)

        self.registers[self.REG_POWERCFG] = powercfg

        self._write_control_registers()

        self._wait_for_stc()

        self._finish_seek()

        status = self.registers[self.REG_STATUSRSSI]

        sfbl = (
            status >> self.STATUS_SFBL
        ) & 1

        if sfbl:
            raise Si4703Error(
                "Seek reached the band limit without finding a station"
            )

        return self.get_frequency()

    def get_frequency(self):
        self._check_initialized()

        self._read_all_registers()

        value = self.registers[self.REG_READCHAN]

        channel = value & 0x03FF

        frequency = 87.5 + (channel * 0.1)

        return frequency

    def get_status(self):
        self._check_initialized()

        self._read_all_registers()

        status = self.registers[self.REG_STATUSRSSI]

        rssi = status & self.STATUS_RSSI_MASK

        stereo = (
            (status >> self.STATUS_STEREO) & 1
        )

        afcrl = (
            (status >> self.STATUS_AFCRL) & 1
        )

        return {
            "rssi": rssi,
            "stereo": bool(stereo),
            "afc_rail": bool(afcrl)
        }

