from flask import Blueprint,Response,request
import json,os,datetime,re
from service import FenceService
from util import TimeUtil

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
        FenceService.insert(time,fenceChange,remain,sms)
        result["result"] = "OK"
        result["time"] = time
        result["fenceChange"] = fenceChange
        result["remain"] = remain
        return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')


    result["result"] = "ERROR"
    result["msg"] = "该笔记录已存在，不能重复添加"
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')