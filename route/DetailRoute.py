from flask import Blueprint,Response,request
import json,datetime
from service import FenceService
from dateutil.relativedelta import relativedelta

detailRoute = Blueprint('detailRoute', __name__)

@detailRoute.route('/getAllInfoByPage',methods=["POST"])
def getAllInfoByPage():
    # 第几页
    pageCount = int(request.form.get("pageCount"))
    # 一页的大小
    pageSize = int(request.form.get("pageSize"))
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    if "" == startTime:
        startTime = "00010101"
    if "" == endTime:
        endTime = "20691231"
    return Response(FenceService.getByPage(startTime, endTime, pageCount, pageSize), mimetype='application/json')

@detailRoute.route('/getTotalPage',methods=["POST"])
def getTotalPage():
    pageSize = int(request.form.get("pageSize"))
    startTime = request.form.get("startTime")
    endTime = request.form.get("endTime")
    if "" == startTime:
        startTime = "00010101"
    if "" == endTime:
        endTime = "20691231"
    allCount = FenceService.getCount(startTime, endTime)
    allPageCount = allCount // pageSize
    if allCount % pageSize != 0:
        return str(allPageCount + 1)
    return str(allPageCount)

@detailRoute.route('/changeReason',methods=["POST"])
def changeReason():
    id = int(request.form.get("id"))
    reason = request.form.get("reason")
    FenceService.changeReason(id, reason)
    return str(FenceService.getById(id)[5])