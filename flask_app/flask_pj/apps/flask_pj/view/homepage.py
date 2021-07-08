import math

from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper

homepage = Blueprint('homepage', __name__, url_prefix='/homepage')

# 已测
@homepage.route('/', methods=[METHODTYPE.POST])
def getHomepage():
    if request.method == METHODTYPE.GET:
        abort(405)
    try:
        user_id = request.values.get("user_id")
        plan_book_info = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
        book_id = plan_book_info["book_id"]["$uuid"]
        book_info = Book.get_one(pk=book_id)
        days = User_Learn_Status.objects(user_id=user_id).count()
        learned_words_numbers = User_Book_Learn_Record.objects(user_id=user_id).count()
        book_learned_words_numbers = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id).count()
        book_all_words_numbers = Word_Book_Correspond.objects(book_id=book_id).count()
        now = constant.get_nowTime()
        today_learn = 0
        word_record_list = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id)
        for word_record in word_record_list:
            if word_record["study_time"].split(" ")[0] == now:
                today_learn += 1
        to_learn = plan_book_info["daily_learn"] + plan_book_info["daily_review"] - today_learn
        left_days = math.ceil((book_all_words_numbers - book_learned_words_numbers) / plan_book_info["daily_learn"])
        return jsonify({"days": days, "words": learned_words_numbers, "book_name": book_info["book_name"],
                        "book_cover": book_info["cover"], "to_learn": to_learn, "left_days": left_days,
                        "total": book_all_words_numbers, "learned": book_learned_words_numbers})
    except Exception as e:
        return jsonify({"days": None, "words": None, "book_name": None, "book_cover": None,
                        "to_learn": None, "left_days": None, "total": None, "learned": None})
