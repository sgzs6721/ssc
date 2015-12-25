#encoding: utf-8
import codecs
import MySQLdb

def getTime(total, number, type) :
    intNumber = int(number)
    hour = 0
    min  = 0
    if type == "cqssc" :
        if total > 72 :
            if intNumber < 24 :
                [hour, min] = calculateTime(intNumber, 0, 0, 5, 0)
            else :
                if intNumber > 96 :
                    [hour, min] = calculateTime(intNumber - 96, 22, 0, 5, 0)
                else :
                    [hour, min] = calculateTime(intNumber - 23, 9, 50, 10, 0)
        else :
            [hour, min] = calculateTime(intNumber, 9, 50, 10, 0)
    elif type == "jxssc" :
        step = calculateStep(intNumber)
        [hour, min] = calculateTime(intNumber, 8, 59, 10, step)

    stringHour = str(hour)
    stringMin  = str(min)

    if hour < 10 :
        stringHour = "0" + stringHour
    if hour == 24 :
        stringHour = "00"
    if min < 10 :
        stringMin  = "0" + stringMin

    return stringHour + ":" + stringMin + ":" + "00"

def calculateStep(number) : #expected : 7767767767764
    bigStep    = 3
    big        = number / 20
    bigReserve = number % 20
    small = bigReserve / 7
    return big * bigStep + small

def calculateTime(intNumber, startHour, startMin, step, adjust) :
    totalMove = intNumber * step  + startMin + adjust
    hour = startHour + totalMove / 60
    min  = totalMove % 60
    return [hour, min]

def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def generateHistory(type) :
    fileObject = codecs.open(type + ".txt", "r", "utf_8_sig")
    dayArray = fileObject.readlines()
    dayArray.reverse()
    datetime = ""
    dayArray = []
    for line in dayArray :
        dataLine = line.replace("-", "")
        info = dataLine.split("\t")
        dateNumber = info[0]
        number     = info[1]
        date       = dateNumber[0:8]
        front3 = checkThree(number[0:3])
        end3   = checkThree(number[2:])
        if not date == datetime :
            if not len(dayArray) == 0 :
                insertDB(dayArray, datetime, type)
                dayArray = []
            dayArray.append([dateNumber, number, front3, end3, "0", "0", "0"])
            datetime = date


def insertDB(array, datetime, type) :
    [dateNumber, number, front3, end3, front4, end4, all] = array
    time = getTime(len(array), dateNumber, type)
    try :
        cur=conn.cursor()
        statement = "insert into " + "`" + type + "`"  + \
        "(`ID`,`date`,`time`,`number`,`front3`,`end3`,`front4`,`end4`,`all`) VALUES (NULL,'" + \
        dateNumber + "','" + time + "','" + number +"','"+ front3 + "','" + end3 + "','" + \
        front4 + "','" + end4 + "','" + all + "')"

        cur.execute(statement)
        cur.close()
        conn.commit()
    except MySQLdb.Error,e:
         print "\tMysql Error %d: %s" % (e.args[0], e.args[1])


host = "localhost"
user = "root"
passwd = "root@lottery"
port = 3306
database = "lottery"

conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')
generateHistory("cqssc") # end 20151202
conn.close()