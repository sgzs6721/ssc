#encoding: utf-8
import utils
import os
from pprint import pprint

# Direct compound
def getLogName(fromDate, toDate, logDir) :
    log = logDir + "/"
    if fromDate == toDate :
        log = log + fromDate
    else :
        log = log + fromDate + "-" + toDate

    return log

def readDataFromFile(type, fromDate, toDate) :
    year  = int(fromDate[0 : 4])
    month = int(fromDate[4 : 6])
    day   = int(fromDate[6 : 8])
    data  = []

    if len(fromDate) == 8 :
        if not(os.path.exists(type + "/" + fromDate) and os.path.exists(type + "/" + toDate)) :
            return data

        while True :
            currentDateGroup = utils.getDate(year, month, day)
            currentDate = currentDateGroup[0]
            [year, month, day] = currentDateGroup[2:]

            fileName = type + "/" + currentDate
            if not os.path.exists(fileName) :
                day = day + 1
                continue
            else :
                fileObject = open(fileName)
                for line in fileObject :
                    data.append(line.strip())
                fileObject.close()
            if currentDate == toDate :
                break
            day = day + 1

        return data
    else :
        # TODO
        return data

def getTimes(star, plan) :
    times = 1
    while star > 0 :
        times = times * plan
        star = star - 1
    return times

def loger() :
    print ""

def simulateDirectBet(fromDate, toDate, type, plan, rebate, times, arrayIndex, logDir) :
    baseInput  = 2
    baseBonus  = 19.44
    if rebate > 0 :
        baseBonus = 18

    inputMoneyOnce = getTimes(len(arrayIndex), plan) * baseInput * (1 - rebate)
    bonusOnce      = baseBonus * (10 ** (len(arrayIndex) - 1))
    inputMoney = 0
    profit     = 0

    log = getLogName(fromDate, toDate, logDir)

    data = readDataFromFile(type, fromDate, toDate)

    pprint(inputMoneyOnce)
    pprint(bonusOnce)
    pprint(log)
    pprint(data)

    return [inputMoney, profit, log]

def simulateGroupBet(fromDate, toDate, type, plan, rebate, times, arrayIndex, logDir) :
    baseInput  = 2
    baseBonus  = 19.44
    if rebate > 0 :
        baseBonus = 18

    inputMoneyOnce = getTimes(len(arrayIndex), plan) * baseInput * (1 - rebate)
    bonusOnce      = baseBonus * (10 ** (len(arrayIndex) - 1))
    inputMoney = 0
    profit     = 0

    log = getLogName(fromDate, toDate, logDir)

    data = readDataFromFile(type, fromDate, toDate)

    pprint(inputMoneyOnce)
    pprint(bonusOnce)
    pprint(log)
    pprint(data)

    return [inputMoney, profit, log]

simulateDirectBet("20151201", "20151201", "CQSSC", 9, 0.072, 1, range(5), "CQLOG")
# simulateGroupBet(20151201, 20151204, "JXSSC", 9, 2, range(2,5), "JXLOG")
# simulateDirectBet(20151201008, 20151201100, "XJSSC", 9, 3, range(1,5), "XJLOG")
