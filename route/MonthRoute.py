from flask import Blueprint,Response,request
import json,datetime,math
from service import FenceService
from dateutil.relativedelta import relativedelta

monthRoute = Blueprint('monthRoute', __name__)


@monthRoute.route('/getTotalInOutByMonth',methods=["POST"])
def getTotalInOutByMonth():
    monthCount = int(request.form.get("monthCount"))
    now_time = datetime.datetime.now()
    firstDayTime = datetime.datetime(now_time.year, now_time.month, 1, 0, 0, 0)
    queryTime = firstDayTime - relativedelta(months=monthCount)
    fences = json.loads(FenceService.getByTime(queryTime))
    result = {}
    for fence in fences:
        ym = datetime.datetime.strftime(
            datetime.datetime.strptime(fence["time"],"%Y-%m-%d %H:%M:%S"),"%Y年%m月")
        if ym not in result:
            result[ym] = {}
            result[ym]["in"] = 0
            result[ym]["out"] = 0
        money = float(fence["fenceChange"])
        if money < 0:
            result[ym]["out"] += money
        else:
            result[ym]["in"] += money
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')


@monthRoute.route('/getLastData', methods=["POST"])
def getLastData():
    return Response(FenceService.getLast(), mimetype='application/json')

@monthRoute.route('/getMonthTongji', methods=["POST"])
def getMonthTongji():
    month = request.form.get("month")
    result = {}
    datas = json.loads(FenceService.getByMonth(month))
    inCount = 0
    outCount = 0
    totalIn = 0
    totalOut = 0
    inList = []
    outList = []
    for data in datas:
        money = float(data["fenceChange"])
        if money < 0:
            outCount += 1
            totalOut += money
            outList.append({"item": data["reason"], "val": math.fabs(money)})
        else:
            inCount += 1
            totalIn += money
            inList.append({"item": data["reason"], "val": money})
    result["inCount"] = inCount
    result["outCount"] = outCount
    result["totalIn"] = totalIn
    result["totalOut"] = math.fabs(totalOut)
    result["inList"] = inList
    result["outList"] = outList
    return Response(json.dumps(result), mimetype='application/json')


@monthRoute.route('/getAllMonth', methods=["POST"])
def getAllMonth():
    return Response(json.dumps(FenceService.getAllMonth()), mimetype='application/json')