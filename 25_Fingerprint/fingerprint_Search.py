import time
import sys
from machine import UART
from pyfingerprint import PyFingerprint
from pyfingerprint import FINGERPRINT_CHARBUFFER1

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
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match!')
        sys.exit()
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))
        
except Exception as e:
    print('Error: ', str(e))
    sys.exit()
