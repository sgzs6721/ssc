#encoding: utf-8
import utils
import os
# from pprint import pprint

def getSplitData(fromDate, toDate, type) :
    data = utils.readDataFromFile(type, fromDate, toDate)

    splitData = []
    for i in range(5) :
        splitData.append([])

    for number in data :
        info       = number.split(" ")
        realNumber = info[2]
        date       = info[0]
        time       = info[1]
        for i in range(5) :
            splitData[i].append(" ".join([realNumber[i], date, time]))

    return splitData

def getBaseInfo(continuedType, number) :
    if continuedType == "even-odd" :
        return number % 2
    else :
        return number > 4

def isLabelExist(index, baseDate, baseNumber, labelDir) :
    return os.path.exists(labelDir + "/" + baseDate + "-" + str(index) + "-" + str(baseNumber))

def writeLabel(index, baseDate, baseNumber, labelDir) :
    fileObject = open(labelDir + "/" + baseDate + "-" + str(index) + "-" + str(baseNumber), "w")
    fileObject.write(baseDate + "-" + str(index) + "-" + str(baseNumber))
    fileObject.close()
    print "writeLabel" + baseDate + "-" + str(index) + "-" + str(baseNumber)

def sendMessage(index, baseDate, baseNumber, labelDir, group):
    content = "index:" + str(index) + "\n"
    content = content + "baseDate:" + baseDate + "\n"
    content = content + "continuedNumber" + group + "\n"
    print content

def continuedNumber(fromDate, toDate, type, continueNumber, continueType, labelDir) :
    if not os.path.exists(labelDir) :
        os.makedirs(labelDir)
    splitData = getSplitData(fromDate, toDate, type)
    maxContinuedNumber   = [1, 1, 1, 1, 1]

    for index, pos in enumerate(splitData) :
        baseNumber = int(pos[0].split(" ")[0])
        baseDate   = pos[0].split(" ")[1]
        base = getBaseInfo(continueType, baseNumber)
        condition = ""
        continued = 1
        i = 1
        group = [baseNumber]
        while i < len(pos) :
            posInfo = pos[i].split(" ")
            condition = getBaseInfo(continueType, int(posInfo[0]))
            if condition == base :
                continued = continued + 1
                group.append(int(posInfo[0]))
                if continued > maxContinuedNumber[index] :
                    maxContinuedNumber[index] = continued
                if continued > 6 :
                    if not isLabelExist(index, baseDate, baseNumber, labelDir) :
                        sendMessage(index, baseDate, baseNumber, labelDir, str(group))
                        writeLabel(index, baseDate, baseNumber, labelDir)
                    else :
                        print "existed " + baseDate

                    print "[" + str(index) + "]" + "(" + str(continued) + ")" + "[" + " ".join([posInfo[1], posInfo[2]]) + "]" + str(group)

            else :
                # Find more than 10 continued detail
                if continued == continueNumber :
                    temp = 1
                    breakNumber = []
                    while True :
                        if condition == getBaseInfo(continueType, int(pos[i + temp].split(" ")[0])) :
                            break
                        temp = temp + 1
                        breakNumber.append(int(pos[i + temp].split(" ")[0]))
                        if i + temp == len(pos) : break
                    # if temp > 6
                    if False :
                        printInfo = "(" + str(index) + ")=>"
                        printInfo = printInfo + str(group) + "=>" + "[" + posInfo[0] + "]"
                        printInfo = printInfo + "(" + " ".join([posInfo[1], posInfo[2]]) + ")" + "=>"
                        printInfo = printInfo + str(breakNumber)
                        printInfo = printInfo + "=>{" + str(temp - 1) + "}"
                        print printInfo
                continued = 1
                base = condition
                group = [int(posInfo[0])]
                baseNumber = int(posInfo[0])
                baseDate   = posInfo[1]
            i = i + 1
    print maxContinuedNumber


continuedNumber("20151208", "20151208", "XJSSC", 6, "even-od", "XJLabel")