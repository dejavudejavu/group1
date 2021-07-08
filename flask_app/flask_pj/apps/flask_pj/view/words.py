import math

from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper

words = Blueprint('words', __name__, url_prefix='/words')


# 已测
@words.route('/', methods=[METHODTYPE.POST])
def getWords():
    if request.method == METHODTYPE.GET:
        abort(405)
    user_id = request.values.get("user_id")
    plan = User_Book_Study_Plan.get_one(user_id=user_id, is_studying=True)
    book_id = plan["book_id"]
    all_words = Word_Book_Correspond.get_list(book_id=book_id)
    words_record = User_Book_Learn_Record.get_list(user_id=user_id, book_id=book_id)
    not_learn_ids = []
    learn_ids = []
    for word in words_record:
        learn_ids.append(word["word_id"])
    for word in all_words:
        word_id = word["word_id"]
        if word_id not in learn_ids:
            not_learn_ids.append(word_id)
    not_learn_words = []
    for word_id in not_learn_ids:
        word_info = Word.get_one(pk=word_id["$uuid"])
        del word_info["_id"]
        del word_info["example"]
        not_learn_words.append(word_info)
    learn_words = []
    for word_id in learn_ids:
        word_info = Word.get_one(pk=word_id["$uuid"])
        del word_info["_id"]
        del word_info["example"]
        learn_words.append(word_info)
    return jsonify({"not_learn": not_learn_words, "learn": learn_words})
