import time
import sys
from machine import UART
from pyfingerprint import PyFingerprint
from pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint import FINGERPRINT_CHARBUFFER2

try:
    f = PyFingerprint(UART(2,57600), 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword()):
        print('Connected successfully and the password in correct.')

    print('Waiting for finger...')
    while ( f.readImage() == False ):
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER1)

    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        sys.exit()

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')
    while ( f.readImage() == False ):
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER2)

    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))

except Exception as e:
    print('Error: ', str(e))
    sys.exit()
