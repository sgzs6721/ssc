#encoding: utf-8
import utils
import os
from pprint import pprint

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

def isLabelExist(type, index, baseDate, labelDir) :
    return os.path.exists(labelDir + "/" + type + "-" + baseDate + "-" + str(index))

def writeLabel(type, continueType, index, baseDate, labelDir, group, times) :
    fileObject = open(labelDir + "/" + continueType + "/" + str(index + 1) + "/" + type + "-" + continueType + "-" + str(times), "a")
    fileObject.write(str(baseDate) + "=>[" + str(index + 1) + "]=>" + str(group) + "\n")
    fileObject.close()
    # print "writeLabel" + baseDate + "-" + str(index) + "=>" + str(group)

def getMessage(type, index, continued, continueType, baseDate, group):
    content = "index:" + str(index) + "\n"
    content = content + "baseDate:" + str(baseDate) + "\n"
    content = content + "continuedNumber" + group + "\n"
    # print content
    return [index, baseDate, group]

def continuedNumber(fromDate, toDate, type, breakNumber, continueType, labelDir) :

    splitData = getSplitData(fromDate, toDate, type)
    maxContinuedNumber   = [1, 1, 1, 1, 1]

    allMessage = []
    timer = 0
    for index, pos in enumerate(splitData) :
        if not os.path.exists(labelDir + "/" + continueType + "/" + str(index + 1)) :
            os.makedirs(labelDir + "/" + continueType + "/" + str(index + 1))
        baseNumber = int(pos[0].split(" ")[0])
        baseDate   = pos[0].split(" ")[1:]
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
            else :
                # Find more than N times continued detail
                # for times in range(15, 25) : # Generate label file
                #     if continued == times :
                #         # writeLabel(type, continueType, index, baseDate, labelDir, group, times)
                #         print "[" + type + "][" + str(index + 1) + "]" + "(" + str(continued) + ")" + str(baseDate) + str(group)

                if continued > breakNumber : # Statistic for break and then continued number
                    temp = 1
                    breakNumbers = []
                    endNumbers   = []

                    drop = 1
                    dropNumbers  = []
                    trend = group[-1] - int(posInfo[0])
                    # while True :
                    while False :
                        if drop + i == len(pos) : break
                        dropNumbers.append(int(pos[i+drop].split(" ")[0]))
                        if trend >= 0 :
                            if int(pos[i+drop].split(" ")[0]) < 5 :
                                break
                        if trend < 0 :
                            if int(pos[i+drop].split(" ")[0]) > 4 :
                                break
                        drop = drop + 1
                    for j in range(1,7) :
                        if i + j == len(pos) :
                            break
                        endNumbers.append(int(pos[i+j].split(" ")[0]))

                    while True :
                    # while False : # Do not calculate break Numbers
                        breakNumbers.append(int(pos[i + temp].split(" ")[0]))
                        # if not int(posInfo[0]) % 2 == int(pos[i+temp].split(" ")[0]) %2 :
                        if condition == getBaseInfo(continueType, int(pos[i + temp].split(" ")[0])) :
                            # for j in range(1,6) :
                            #     if i + temp + j == len(pos) :
                            #         break
                            #     endNumbers.append(int(pos[i+temp+j].split(" ")[0]))
                            break
                        temp = temp + 1
                        if i + temp == len(pos) : break
                    if temp >= 6 :
                    # if drop >= 6 :
                        timer = timer + 1
                        printInfo = str(timer) + "(" + str(index) + ")=>[" + str(continued) + "]"
                        printInfo = printInfo + str(group) + "=>" + "[" + posInfo[0] + "]"
                        printInfo = printInfo + "(" + " ".join([posInfo[1], posInfo[2]]) + ")"
                        printInfo = printInfo + "=>" + str(breakNumbers)
                        printInfo = printInfo + "=>{" + str(temp) + "}"
                        # printInfo = printInfo + "=>" + str(dropNumbers)
                        # printInfo = printInfo + "=>{" + str(drop) + "}"
                        # printInfo = printInfo + str(endNumbers)
                        print printInfo
                continued = 1
                base = condition
                group = [int(posInfo[0])]
                baseDate   = posInfo[1:]
            i = i + 1
    print maxContinuedNumber # Find the max continued number
    return allMessage

# Statistic for continued number and break continued number
# for type in ["even-odd", "size"] :
#     continuedNumber("20070401", "20151202", "CQSSC", 6, type, "CQLabel")
#     continuedNumber("20080928", "20151202", "JXSSC", 6, type, "JXLabel")
#     continuedNumber("20070812", "20151208", "XJSSC", 6, type, "XJLabel")
continuedNumber("20070812", "20151202", "XJSSC", 6, "even-odd", "XJLabel")
