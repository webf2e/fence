from flask import Blueprint,Response,request
import json,os,datetime
from service import FenceService

indexRoute = Blueprint('indexRoute', __name__)

@indexRoute.route('/current',methods=["POST"])
def current():
    return Response(FenceService.getLast(), mimetype='application/json')

@indexRoute.route('/getInOutFences',methods=["POST"])
def getInOutFences():
    count = request.form.get("count")
    return Response(FenceService.getFences(count), mimetype='application/json')

@indexRoute.route('/getHisFences',methods=["POST"])
def getHisFences():
    count = request.form.get("count")
    return Response(FenceService.getFences(count), mimetype='application/json')