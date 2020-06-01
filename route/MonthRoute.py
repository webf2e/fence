from flask import Blueprint,Response,request
import json,datetime
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


@monthRoute.route('/getAllInfoByPage',methods=["POST"])
def getAllInfoByPage():
    # 第几页
    pageCount = int(request.form.get("pageCount"))
    # 一页的大小
    pageSize = int(request.form.get("pageSize"))
    return Response(FenceService.getByPage(pageCount, pageSize), mimetype='application/json')

@monthRoute.route('/getTotalPage',methods=["POST"])
def getTotalPage():
    pageSize = int(request.form.get("pageSize"))
    allCount = FenceService.getCount()
    allPageCount = allCount // pageSize
    if allCount % pageSize != 0:
        return str(allPageCount + 1)
    return str(allPageCount)

@monthRoute.route('/changeReason',methods=["POST"])
def changeReason():
    id = int(request.form.get("id"))
    reason = request.form.get("reason")
    FenceService.changeReason(id, reason)
    return str(FenceService.getById(id)[5])
