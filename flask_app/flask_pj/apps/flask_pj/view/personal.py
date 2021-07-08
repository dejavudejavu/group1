import math

from flask import Blueprint, jsonify, current_app, request, abort
from werkzeug.exceptions import LengthRequired
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper, constants

personal = Blueprint('personal', __name__, url_prefix='/personal')

# 已测
@personal.route('/getClockons', methods=[METHODTYPE.POST])
def getClockons():
    if request.method == METHODTYPE.GET:
        abort(405)
    user_id = request.values.get("user_id")
    status = User_Learn_Status.objects(user_id=user_id).order_by('-clockons')
    status = jsonHelper.bsonCollectionToDict(status)
    clockons, max_length, length = [], 0, 0
    clockons.append(status[0]['clockons'])
    for i in range(len(status)-1):
        clockons.append(status[i+1]['clockons'])
        if constants.get_days(clockons[i], clockons[i+1]) == 1:
            length += 1
        else:
            if length > max_length:
                max_length = length
            length = 0
    if length > max_length:
        max_length = length
    if max_length != 0:
        max_length += 1
    return jsonify({"max_length": max_length, "clockons": clockons})
