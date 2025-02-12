import re

def sumOnOff(texto):

    sumActive = True
    total_sum = 0

    for match in re.finditer(r'(\d+|off|on|=)', texto, flags=re.IGNORECASE):
        item = match.group(0).lower()
        
        if item == 'off':
            sumActive = False
        elif item == 'on':
            sumActive = True
        elif item == '=':
            print(total_sum)
        elif sumActive:
            total_sum += int(item)

texto = """dsadwadadsadaw45adwadsadw2025-02-07sdadaw=OFFdwasfgsdf789dsadwadsad43dwaONdsadw2adsadasON5=sdadw45dwa2025fgsdOFFdsadsfON987sdONsadw789sdONsd5=2025ON3dwaONdsadw777ON543sdad="""
sumOnOff(texto)