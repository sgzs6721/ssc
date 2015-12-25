#encoding: utf-8
import urllib2
import time
from BeautifulSoup import BeautifulSoup

import MySQLdb

def getBeautifulSoup(url) :
    req = urllib2.Request(url)
    res =urllib2.urlopen(req).read()
    soup = BeautifulSoup(res)
    return soup

def insertXJ(soup, fileName) :
    tableTr = soup.table.findAll("tr")
    realTr = tableTr[ 3 : -2 ]

    for tr in realTr :
        realTd = tr.findAll("td")[0:3]
        if realTd[2].text.encode("utf8") == "&nbsp;" :
            print  fileName + ", no data!"
            return
        else :
            date = realTd[0].text.encode("utf8")
            dataNumber = realTd[2].text.encode("utf8").replace(" ",'')
            print realTd[2].text.encode("utf8")

            insertDB(date,
                     date[0:8] + " " + realTd[1].text.encode("utf8"),
                     dataNumber, checkThree(dataNumber[0:3]),
                     checkThree(dataNumber[2:]),
                     "0", "0", "0",
            )

    print fileName + " Done!"

def insertDB(dateNumber, time, number, front3, end3, front4, end4, all) :
    try :
        cur=conn.cursor()
        statement = "insert into " + "`xjssc`"  + \
        "(`ID`,`date`,`time`,`number`,`front3`,`end3`,`front4`,`end4`,`all`) VALUES (NULL,'" + \
        dateNumber + "','" + time + "','" + number +"','"+ front3 + "','" + end3 + "','" + \
        front4 + "','" + end4 + "','" + all + "')"

        cur.execute(statement)
        cur.close()
        conn.commit()
    except MySQLdb.Error,e:
         print "\tMysql Error %d: %s" % (e.args[0], e.args[1])

def checkThree(dataNumber) :
    if dataNumber[0] == dataNumber[1] :
        return "1"
    if dataNumber[0] == dataNumber[2] :
        return "1"
    if dataNumber[1] == dataNumber[2] :
        return "1"
    return "0"

def isDateValidate(date) :
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def getHistoryXJ(dateYear, dateMonth, dateDay) :
    currentDate = getDate(dateYear, dateMonth, dateDay)
    fromDate = currentDate[0]
    [dateYear, dateMonth, dateDay] = currentDate[2:]
    endDate = getDate(dateYear, dateMonth, dateDay + 1)[0]

    url = "http://www.xjflcp.com/trend/analyseSSC.do?operator=goldSscTrend&type=draw&drawBegin="\
     + fromDate + "&drawEnd=" + endDate
    s = getBeautifulSoup(url)
    insertXJ(s, fromDate)

    return [dateYear, dateMonth, dateDay]

def getDate(year,month,day) :
    stringMonth = str(month)
    stringDay   = str(day)

    if day < 10 :
        stringDay = "0" + stringDay
    elif day > 31 :
        day = 1
        stringDay = "01"
        month = month + 1
        stringMonth = str(month)
    if month < 10 :
        stringMonth = "0" + stringMonth
    if month > 12 :
        month = 1
        stringMonth = "01"
        year = year + 1
    stringYear  = str(year)

    formatDate = stringYear + "-" + stringMonth + "-" + stringDay
    if isDateValidate(formatDate) :
        return [stringYear + stringMonth + stringDay, formatDate, year, month, day]
    else :
        day = day + 1
        return getDate(year, month, day)

def getAllHistoryXJ(year, month, day) :
    while True :
        if year == time.localtime()[0] and month == time.localtime()[1] and day == time.localtime()[2] :
            break
        [year, month, day] = getHistoryXJ(year, month, day)
        day = day + 1

host = "localhost"
user = "root"
passwd = "root@lottery"
port = 3306
database = "lottery"

conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')
getAllHistoryXJ(2012, 1, 22) # end current date
conn.close()
