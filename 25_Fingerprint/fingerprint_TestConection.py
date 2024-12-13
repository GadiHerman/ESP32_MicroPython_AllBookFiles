from machine import UART
import sys
from pyfingerprint import PyFingerprint

try:
    f = PyFingerprint(UART(2,57600), 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword()):
        print('Connected successfully and the password in correct.')
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    else:
        print('The fingerprint sensor password is wrong.')
        sys.exit()
    
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    sys.exit()
