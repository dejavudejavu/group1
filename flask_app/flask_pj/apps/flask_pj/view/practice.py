import random

from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper

practice = Blueprint('practice', __name__, url_prefix='/practice')


# 已测
@practice.route('/getWords', methods=[METHODTYPE.POST])
def api_practice():
    user_id = request.values.get("user_id")
    source = int(request.values.get("source"))
    user_plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
    book_id = user_plan["book_id"]["$uuid"]
    now = constant.get_nowTime()
    all_words = Word_Book_Correspond.get_list(book_id=book_id)
    to_learn_words_id = get_to_learn_words_id_list(source, user_plan, user_id, book_id, all_words)
    # 根据id列表来获取词
    to_learn_words = []
    for word_id in to_learn_words_id:
        word_info = Word.get_one(word_id=word_id)
        wrong_ids = [word_id]
        wrong_choices = []
        for i in range(0, 3):
            wrong_id = random.choice(all_words)["word_id"]["$uuid"]
            if wrong_id in wrong_ids:
                continue
            wrong_ids.append(wrong_id)
            wrong_word = Word.get_one(word_id=wrong_id)
            wrong_choices.append(wrong_word["explanation"])
            i += 1
        examples = word_info["example"].split("\n")
        del word_info["example"]
        word_info["examples"] = examples
        try:
            words_record = User_Book_Learn_Record.get_one(user_id=user_id, book_id=book_id,word_id=word_id)
            word_info["is_in_wrongwords"] = words_record["is_incorrect"]
        except:
            word_info["is_in_wrongwords"] = False
        word_info["wrong_choices"] = wrong_choices
        to_learn_words.append(word_info)
    return jsonify(to_learn_words)


@practice.route('/wrongWords', methods=[METHODTYPE.POST])
def api_wrong_word():
    user_id = request.values.get("user_id")
    word_id = request.values.get("word_id")
    action = int(request.values.get("action"))
    book_id = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)["book_id"]["$uuid"]
    print(book_id)
    now = constant.get_nowTime()
    try:
        # try:
        word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
        # except:
        #     word_Record = User_Book_Learn_Record(user_id=user_id, book_id=book_id, word_id=word_id, is_incorrect=False,
        #                                          is_star=False, study_time=now)
        #     word_Record.save()
        #     word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
        print(word_Record)
        if action == 1:
            word_Record.update(set__is_incorrect=True)
        elif action == 2:
            word_Record.update(set__is_incorrect=False)
        else:
            msg = "action参数错误"
            return msg
        word_Record.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@practice.route('/click', methods=[METHODTYPE.POST])
def api_click_word():
    user_id = request.values.get("user_id")
    word_id = request.values.get("word_id")
    try:
        # study_time = constant.get_review_time(2)
        study_time = constant.get_nowTime()
        detail_time = constant.get_detail_time()
        learn_plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = learn_plan["book_id"]["$uuid"]
        test_status_count = User_Learn_Status.objects(user_id=user_id, clockons=study_time).count()
        if test_status_count == 0:
            status = User_Learn_Status(user_id=user_id, clockons=study_time, learn_amount=0, review_amount=0)
            status.save()
        status = User_Learn_Status.objects.get(user_id=user_id, clockons=study_time)
        status_dict = jsonHelper.bsonToDict_withID(status)
        word_count = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id, word_id=word_id).count()
        if word_count == 0:
            book = Book.objects.get(pk=book_id)
            word = Word.objects.get(pk=word_id)
            word_Record = User_Book_Learn_Record(user_id=user_id, book_id=book, word_id=word, is_incorrect=False,
                                                 is_star=False, study_time=detail_time)
            word_Record.save()
            status.update(set__learn_amount=status_dict["learn_amount"] + 1)
        else:
            word_Record = User_Book_Learn_Record.objects.get(user_id=user_id, book_id=book_id, word_id=word_id)
            word_Record.update(set__study_time=detail_time)
            word_Record.save()
            status.update(set__review_amount=status_dict["review_amount"] + 1)
        status.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


def get_to_learn_words_id_list(source, user_plan, user_id, book_id, all_words):
    all_words_id = []
    for words in all_words:
        all_words_id.append(words["word_id"]["$uuid"])
    now = constant.get_nowTime()
    if source == 1:
        today_learn = 0
        try:
            words_id_record = []
            words_record = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id)
            for word_record in words_record:
                words_id_record.append(word_record["word_id"]["$uuid"])
                if word_record["study_time"].split(" ")[0] == now:
                    today_learn += 1
        except:
            words_id_record = []
        to_learn = user_plan["daily_learn"] - today_learn
        total_size = 0
        size = 0
        to_learn_words_id = []
        # 获取每天学习的内容
        for word_id in all_words_id:
            # 判断size是否足够每天的计划
            if size >= to_learn:
                break
            if word_id in words_id_record:
                continue
            else:
                to_learn_words_id.append(word_id)
                size += 1
                total_size += 1
                if total_size == 10:
                    return to_learn_words_id
        # 获取每天复习的内容
        if to_learn > 0:
            to_review = user_plan["daily_review"]
        else:
            to_review = user_plan["daily_review"] + to_learn
        size = 0
        try:
            words_record = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id).order_by("study_time")
            words_record = jsonHelper.bsonCollectionToDict(words_record)
        except:
            words_record = []
        for word in words_record:
            # 判断size是否足够每天的计划
            if size >= to_review:
                break
            to_learn_words_id.append(word["word_id"]["$uuid"])
            size += 1
            total_size += 1
            if total_size == 10:
                return to_learn_words_id
    else:
        try:
            to_learn_words_id = User_Book_Learn_Record.get_list(
                user_id=user_id, book_id=book_id, is_incorrect=True)
            to_learn_words_id = to_learn_words_id[:10]
        except:
            to_learn_words_id = []
    return to_learn_words_id
