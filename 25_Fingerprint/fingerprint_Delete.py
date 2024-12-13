import sys
from machine import UART
from pyfingerprint import PyFingerprint

try:
    f = PyFingerprint(UART(2,57600), 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword()):
        print('Connected successfully.')
        
    print('Used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    tableIndex = f.getTemplateIndex(0)
    for i in range(0, len(tableIndex)):
        if tableIndex[i]:
            print('Fingerprint at position #' + str(i) + ' is in used. ')

    positionNumber = int(input('Enter the Fingerprint position you want to delete: '))
    if ( f.deleteTemplate(positionNumber) == True ):
        print('Template deleted!')

    print('Used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    tableIndex = f.getTemplateIndex(0)
    for i in range(0, len(tableIndex)):
        if tableIndex[i]:
            print('Fingerprint at position #' + str(i) + ' is in used. ')

except Exception as e:
    print('Error: ', str(e))
    sys.exit()
