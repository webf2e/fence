from flask import Blueprint,Response,request
import json,os,datetime,re,math
from service import FenceService
from dateutil.relativedelta import relativedelta
from util import TimeUtil,PushUtil

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