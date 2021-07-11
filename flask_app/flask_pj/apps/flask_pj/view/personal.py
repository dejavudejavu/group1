from flask import Blueprint, jsonify, request, abort

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils import jsonHelper, constants
from flask_pj.apps.utils.constants import METHODTYPE

personal = Blueprint('personal', __name__, url_prefix='/personal')


# 已测
@personal.route('/getClockons', methods=[METHODTYPE.POST])
def getClockons():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        user_id = request.values.get("user_id")
        status = User_Learn_Status.objects(user_id=user_id, is_clockin=True)
        status_count = status.count()
        if status_count == 0:
            return jsonify({"msg": "成功", "max_length": 0, "clockons": []})
        status = status.order_by('-clockons')
        status = jsonHelper.bsonCollectionToDict(status)
        clockons, max_length, length = [], 0, 0
        clockons.append(status[0]['clockons'])
        for i in range(len(status) - 1):
            clockons.append(status[i + 1]['clockons'])
            if constants.get_days(clockons[i], clockons[i + 1]) == 1:
                length += 1
            else:
                if length > max_length:
                    max_length = length
                length = 0
        if length > max_length:
            max_length = length
        if max_length != 0:
            max_length += 1
        if len(status) == 1:
            max_length = 1
        return jsonify({"msg": "成功", "max_length": max_length, "clockons": clockons})
    except Exception as e:
        return jsonify({"msg": str(e), "max_length": None, "clockons": None})


@personal.route('/clockin', methods=[METHODTYPE.POST])
def clockin():
    try:
        study_time = constants.get_nowTime()
        user_id = request.values.get("user_id")
        status = User_Learn_Status.objects(user_id=user_id, clockons=study_time)
        status_count = status.count()
        if status_count == 0:
            msg = "未达成学习目标"
        else:
            plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
            book_id = plan["book_id"]["$uuid"]
            now = constants.get_nowTime()
            today_learn = 0
            word_records = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
            for word_record in word_records:
                if word_record["study_time"].split(" ")[0] == now:
                    today_learn += 1
            to_learn = plan["daily_learn"] + plan["daily_review"] - today_learn
            if to_learn > 0:
                msg = "未达成学习目标"
            else:
                status = status.first()
                if jsonHelper.bsonToDict(status)["is_clockin"] == False:
                    status.update(set__is_clockin = True)
                    status.save()
                    msg = "成功"
                else:
                    msg = "今日已打卡"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@personal.route('/share', methods=[METHODTYPE.POST])
def share():
    try:
        study_time = constants.get_nowTime()
        user_id = request.values.get("user_id")
        user_avatar = User.get_one(pk=user_id)["avatar"]
        clockin_amount = User_Learn_Status.objects(user_id=user_id, is_clockin=True).count()
        status = User_Learn_Status.get_one(user_id=user_id, clockons=study_time)
        today_learn = status["learn_amount"] + status["review_amount"]
        return jsonify({"msg": "成功", "avatar": user_avatar, "today_learn": today_learn, "clockin_amount": clockin_amount})
    except Exception as e:
        return jsonify({"msg": str(e), "avatar": None, "today_learn": None, "clockin_amount": None})