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

                if continued == breakNumber : # Statistic for break and then continued number
                    temp = 1
                    breakNumbers = []
                    while True :
                    # while False : # Do not calculate break Numbers
                        if condition == getBaseInfo(continueType, int(pos[i + temp].split(" ")[0])) :
                            break
                        temp = temp + 1
                        breakNumbers.append(int(pos[i + temp].split(" ")[0]))
                        if i + temp == len(pos) : break
                    if temp > 4 :
                    # if False : # Do not show break Numbers
                        timer = timer + 1
                        printInfo = "(" + str(index) + ")=>[" + str(continued) + "]"
                        printInfo = printInfo + str(group) + "=>" + "[" + posInfo[0] + "]"
                        printInfo = printInfo + "(" + " ".join([posInfo[1], posInfo[2]]) + ")" + "=>"
                        printInfo = printInfo + str(breakNumbers)
                        printInfo = printInfo + "=>{" + str(temp - 1) + "}"
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
continuedNumber("20140101", "20151108", "CQSSC", 6, "even-od", "XJLabel")