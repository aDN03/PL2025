import re

def sumOnOff(texto):

    sumActive = False
    sum = 0
    resultado = []
    

    for match in re.finditer(r'(\d+|off|on|=)', texto, flags=re.IGNORECASE):
        item = match.group(0).lower()
        
        if item == 'off':
            sumActive = False
        elif item == 'on':
            sumActive = True
        elif item == '=':
            resultado.append(sum)
            sum = 0
        elif item.isdigit() and sumActive:
            sum += int(item)
    
    return resultado

texto = "dsadwadadsadaw45adwadsadw2025-02-07sdadaw=OFFdwasfgsdf789dsadwadsad43dwaONdsadw2adsadasON5="
resultados = sumOnOff(texto)

for resultado in resultados:
    print(resultado)