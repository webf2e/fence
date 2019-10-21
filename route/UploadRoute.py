from flask import Blueprint,Response,request
import json,os,datetime,re,math
from service import FenceService
from util import TimeUtil,PushUtil

uploadRoute = Blueprint('uploadRoute', __name__)

@uploadRoute.route('/uploadFence',methods=["POST"])
def uploadFence():
    result = {}
    try:
        sms = str(request.form.get("sms")).strip()
        inOrOut = ""
        if sms.find("支出") != -1:
            inOrOut = "-"
        date = re.search("\d*[月]\d*[日]\d*[时]\d*[分]", sms)
        time = TimeUtil.getFullTime(date.group(0))

        fenceChange = inOrOut + sms.split("人民币")[1].split("元")[0]

        remain = sms.split("活期余额")[1].split("元")[0]
    except Exception as e:
        print(e)
        result["result"] = "ERROR"
        result["msg"] = "短信内容可能有问题，请检查哦"
        return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')

    if not FenceService.isExist(time,remain):
        lastRemain = json.loads(FenceService.getLast())[0]["remain"]
        FenceService.insert(time,fenceChange,remain,sms)
        result["result"] = "OK"
        result["time"] = time
        result["fenceChange"] = fenceChange
        result["remain"] = remain
        try:
            PushUtil.pushToSingle("资金有变动", "当前余额为：" + remain, "")
            # 判断是否当前余额 == 上次余额 + 本次支出
            print("lastRemain:{}, fenceChange:{}, remain:{}".format(lastRemain,fenceChange,remain))
            minus = math.fabs(float(lastRemain) + float(fenceChange) - float(remain))
            if minus > 1:
                PushUtil.pushToSingle("资金余额有问题", "余额有" + str(minus) + "的差值", "")
        except Exception as e:
            print("发送通知失败")
        return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')
    result["result"] = "ERROR"
    result["msg"] = "该笔记录已存在，不能重复添加"
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')