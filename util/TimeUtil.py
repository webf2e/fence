import datetime

def getFullTime(MonthDayHourMin):
    currentYear = datetime.datetime.now().year
    currentTimestamp = datetime.datetime.now().timestamp()
    fullDate = "{}年{}".format(currentYear,MonthDayHourMin)
    date = datetime.datetime.strptime(fullDate,"%Y年%m月%d日%H时%M分")
    timestamp = date.timestamp()
    if currentTimestamp > timestamp:
        return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    currentYear = currentYear - 1
    fullDate = "{}年{}".format(currentYear, MonthDayHourMin)
    date = datetime.datetime.strptime(fullDate, "%Y年%m月%d日%H时%M分")
    return datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")