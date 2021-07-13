import requests
import json
from flask import Blueprint, jsonify, request, abort

from flask_pj.apps.flask_pj.model import *
from flask_pj.apps.utils import jsonHelper, constants
from flask_pj.apps.utils.constants import METHODTYPE
from flask_pj.apps import *
import flask_pj.apps.utils.constants as constant

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
        user = User.get_one(user_id=user_id)
        return jsonify({"msg": "成功", "max_length": max_length, "clockons": clockons, "is_remind": user["is_remind"],
                        "remind_time": user["remind_time"]})
    except Exception as e:
        return jsonify({"msg": str(e), "max_length": None, "clockons": None, "is_remind": None, "remind_time": None})


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
                    status.update(set__is_clockin=True)
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
        return jsonify(
            {"msg": "成功", "avatar": user_avatar, "today_learn": today_learn, "clockin_amount": clockin_amount})
    except Exception as e:
        return jsonify({"msg": str(e), "avatar": None, "today_learn": None, "clockin_amount": None})


def set_one_message(user_id):
    try:
        plan_book_info = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan_book_info["book_id"]["$uuid"]
        now = constant.get_nowTime()
        today_learn = 0
        word_record_list = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, is_studying=True)
        for word_record in word_record_list:
            if word_record["study_time"].split(" ")[0] == now:
                today_learn += 1
        to_learn = plan_book_info["daily_learn"] - today_learn
        if to_learn < 0:
            to_review = to_learn + plan_book_info["daily_review"]
            to_learn = 0
        else:
            to_review = plan_book_info["daily_review"]
        if to_review < 0:
            to_review = 0
        print(to_review)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        }
        response = requests.get(url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid"
                                    "=wxfacc648774646439&secret=d1148882a0a2e922a4493c0dd1913102", headers=headers)
        access_token = response.json()["access_token"]
        if access_token:
            data = {
                # "access_token": access_token,
                "touser": user_id,
                "template_id": "bNEVQXRERG9H1mQxGf-ctuarD8FNPmt81eqhypD--L4",
                "page": "/pages/homepage/homepage",
                "data":
                    {
                        "number3":
                            {
                                "value": to_learn
                            },
                        "number4":
                            {
                                "value": to_review
                            }
                    },
            }
            print(data)
            data = json.dumps(data)
            headers={
                'WebRequest.ContentType' : "application/x-www-form-urlencoded",
            }
            message_response = requests.post(
                url="https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}".format(access_token),
                data=data, headers=headers)
            msg = "成功" if message_response.status_code == 200 else "发送失败"
        else:
            msg = "未能返回正确的access_token"
        print(msg)
        return jsonify({"msg": msg})
    except Exception as e:
        return jsonify({"msg": "失败"})


@personal.route('/sendMessage', methods=[METHODTYPE.POST])
def set_message():
    # try:
    user_id = request.values.get("user_id")
    user = User.objects.get(user_id=user_id)
    remind_time = request.values.get("time")
    action = int(request.values.get("action"))
    if action == 1:
        # scheduler.add_job(func="set_one_message", trigger="cron", id=user_id, args=[user_id],
        #                     hour=int(remind_time.split(':')[0]),
        #                     minute=int(remind_time.split(':')[1]))
        # scheduler.start()
        print("设置message")
        set_one_message(user_id)
        print("发送消息结束")
        user.update(set__is_remind=True)
        user.update(set__remind_time=remind_time)
        user.save()
    elif action == 2:
        # scheduler.remove_job(id=user_id)
        user.update(set__is_remind=False)
        user.save()
    else:
        scheduler.remove_job(id=user_id)
        scheduler.add_job(func="set_one_message", trigger="cron", id=user_id, args=[user_id],
                            hour=int(remind_time.split(':')[0]),
                            minute=int(remind_time.split(':')[1]))
        scheduler.start()
        user.update(set__remind_time=remind_time)
        user.save()
    return jsonify({"msg": "成功"})
    # except Exception as e:
    #     return jsonify({"msg": str(e)})
