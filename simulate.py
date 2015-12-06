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

def readLastLine(type, fromDate) :
    year  = int(fromDate[0 : 4])
    month = int(fromDate[4 : 6])
    day   = int(fromDate[6 : 8])

    if len(fromDate) == 8 :
        day = day - 1
        if day == 0 :
            day = 31
            month = month - 1
            if month == 0 :
                month = 12
                year = year - 1

        strMonth = str(month)
        strDay   = str(day)
        if month < 10 :
            strMonth = "0" + strMonth
        if day < 10 :
            strDay = "0" + strDay

        groupDate = str(year) + strMonth + strDay
        dateFile = type + "/" + groupDate

        if utils.isDateValidate(str(year) + "-" + strMonth + "-" + strDay) :
            if os.path.exists(dateFile) :
                fileObject = open(dateFile)
                lastLine = fileObject.readlines()[-1].strip()
                fileObject.close()
                return lastLine
            else :
                return readLastLine(type, groupDate)
        else :
            return readLastLine(type, groupDate)

def getTimes(star, plan) :
    times = 1
    while star > 0 :
        times = times * plan
        star = star - 1
    return times

def loger() :
    print ""

def isFirstDay(type, date) :
    if type == "CQSSC" :
        if date == "20070401" :
            return True
    if type == "JXSSC" :
        if date == "20080928" :
            return True
    if type == "XJSSC" :
        if date == "20070812" :
            return True
    return False

def getNumber(line) :
    info = line.split(" ")
    date = info[0]
    time = info[1]
    number = info[2]
    f3     = info[3]
    b3     = info[4]
    return [date, time, number, f3, b3]

def simulateDirectBet(fromDate, toDate, type, plan, rebate, times, arrayIndex, logDir) :
    baseInput  = 2
    baseBonus  = 19.44
    if rebate > 0 :
        baseBonus = 18

    inputMoneyOnce = getTimes(len(arrayIndex), plan) * baseInput * (1 - rebate)
    bonusOnce      = baseBonus * (10 ** (len(arrayIndex) - 1))
    # inputMoney = 0
    profit     = 0

    log = getLogName(fromDate, toDate, logDir)

    data = readDataFromFile(type, fromDate, toDate)

    baseline = ""
    if isFirstDay(type,fromDate) : # first day
        baseline = data[0]
        data = data[1:]
    else :
        baseline = readLastLine(type, fromDate)

    baseNumber = baseline.split(" ")[2]
    baseDate   = baseline.split(" ")[0]

    if len(data) == 0 :
        print "NO DATA!"
        exit()


    continued = 1
    maxContinued = continued
    totalHit  = 0
    for line in data :
        info = line.split(" ")
        number = info[2]
        date   = info[0]
        hit    = False
        thisInput  = inputMoneyOnce * times
        thisBonus  = 0
        print "Compare " + number + "(" + date + ")" + " with " + baseNumber + "(" + baseDate + ")"
        for index in arrayIndex :
            if number[index] == baseNumber[index] :
                hit = True
                totalHit = totalHit + 1
                continued = continued + 1
                if continued > maxContinued :
                    maxContinued = continued
                print "Fail to get bonus"
                break
        if not hit :
            continued = 1
            thisBonus  = bonusOnce * times
            print "Get bonus " + str(thisBonus)
        baseNumber = number
        baseDate   = date
        profit = profit + thisBonus - thisInput

    maxInputMoney = (continued - 1) * inputMoneyOnce * times

    print inputMoneyOnce
    print profit
    print maxContinued - 1
    print totalHit
    return [profit, maxInputMoney]

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

    # pprint(inputMoneyOnce)
    pprint(bonusOnce)
    pprint(log)
    pprint(data)

    return [inputMoney, profit, log]

simulateDirectBet("20130209", "20130209", "XJSSC", 9, 0, 1, range(5), "CQLOG")
# simulateGroupBet(20151201, 20151204, "JXSSC", 9, 2, range(2,5), "JXLOG")
# simulateDirectBet(20151201008, 20151201100, "XJSSC", 9, 3, range(1,5), "XJLOG")
