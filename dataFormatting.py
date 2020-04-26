filein = input("Enter Filename: ")

with open(filein,'r') as file:
    lines = file.readlines()

    fileout = filein.replace('1','2')
    outFile = open(fileout, 'w')

    for line in lines:
        outputLine = ""
        splitLine = line.split()

        if "a08" in splitLine[0]:
            outputLine = "8 "
        elif "a10" in splitLine[0]:
            outputLine = "10 "
        elif "a12" in splitLine[0]:
            outputLine = "12 "
        elif "a13" in splitLine[0]:
            outputLine = "13 "
        elif "a15" in splitLine[0]:
            outputLine = "15 "
        elif "a16" in splitLine[0]:
            outputLine = "16 "
        else:
            print("Unknown Label")

        index = 1
        for elem in splitLine[1:]:
            elem = elem.replace('[','')
            elem = elem.replace(',','')
            elem = elem.replace(']','')

            outputLine += str(index) + ":" + elem + " "
            index += 1

        outFile.write(outputLine + "\n")
