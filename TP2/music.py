import sys
import re

division_pattern = re.compile(r';')

sys.stdin.readline()
lines = sys.stdin.readlines()

composers = [] 
piecesPerPeriod = []
periodTitles = {}

current_line = ''
inside_quotes = False

for line in lines:
    line = line.strip()
    
    if line:
        current_line += line

    if '.";' in current_line:

        processedLine = current_line.split('.";')
        processedLine1 = processedLine[0].split(';', 1)
        finalLine = processedLine1[0] + processedLine[1]

        fields = division_pattern.split(finalLine)
        
        fields = [field.replace('""', 'TEMP_QUOTE').replace('"', '') for field in fields]
        
        fields = [field.replace('TEMP_QUOTE', '"') for field in fields]


        if fields[2] not in composers:
            composers.append(fields[2])

        found = False
        for i, (period, count) in enumerate(piecesPerPeriod):
            if period == fields[1]:
                piecesPerPeriod[i] = (period, count + 1)
                found = True
                break

        if not found:
            piecesPerPeriod.append((fields[1], 1))

        if fields[1] not in periodTitles:
            periodTitles[fields[1]] = []

        periodTitles[fields[1]].append(fields[0])

        current_line = ''

for period in periodTitles:
    periodTitles[period].sort()

composers.sort()


#print("Composers:", composers)
#print("Pieces per Period:", piecesPerPeriod)
print("Period Titles:", periodTitles)
