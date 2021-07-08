import math

from flask import Blueprint, jsonify, current_app, request, abort
from flask_pj.apps.utils.constants import METHODTYPE
import flask_pj.apps.utils.constants as constant
from flask_pj.apps.flask_pj.model import *
from bson import json_util
import json
from flask_pj.apps.utils import jsonHelper

changeBook = Blueprint('changeBook', __name__, url_prefix='/changeBook')


@changeBook.route('/getMyBooks', methods=[METHODTYPE.POST])
def getMyBooks():
    if request.method == METHODTYPE.GET:
        abort(405)
    user_id = request.values.get("user_id")
    plans = User_Book_Study_Plan.get_list(user_id=user_id)
    books = []
    for plan in plans:
        print(plan)
        book_id = plan["book_id"]["$uuid"]
        book = Book.get_one(book_id=book_id)
        word_amount = Word_Book_Correspond.objects(book_id=book_id).count()
        word_learnt = User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id).count()
        word_to_learn = word_amount - word_learnt
        books.append({"book_cover": book["cover"], "book_name": book["book_name"], "words": word_amount,
                      "to_learn": word_to_learn})
    return jsonify(books)


@changeBook.route('/deleteBook', methods=[METHODTYPE.POST])
def deleteBook():
    try:
        user_id = request.values.get("user_id")
        book_id = request.values.get("book_id")
        plan = User_Book_Study_Plan.objects.get(user_id=user_id, book_id=book_id)
        user_book_plan = jsonHelper.bsonToDict(plan)
        if user_book_plan["is_studying"]:
            try:
                new_plan = User_Book_Study_Plan.objects(user_id=user_id, is_studying=False).first()
                new_plan.update(set__is_studying=True)
                new_plan.save()
                plan.delete()
                msg = "成功"
            except:
                msg = "不要删除唯一一本书嘛"
        else:
            plan.delete()
            msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@changeBook.route('/clearProgress', methods=[METHODTYPE.POST])
def clearProgress():
    try:
        user_id = request.values.get("user_id")
        book_id = request.values.get("book_id")
        User_Book_Learn_Record.objects(user_id=user_id, book_id=book_id).delete()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})


@changeBook.route('/change', methods=[METHODTYPE.POST])
def change():
    try:
        user_id = request.values.get("user_id")
        book_id = request.values.get("book_id")
        plan = User_Book_Study_Plan.objects.get(is_studying=True)
        plan.update(set__is_studying=False)
        plan.save()
        plan = User_Book_Study_Plan.objects.get(user_id=user_id, book_id=book_id)
        plan.update(set__is_studying=True)
        plan.save()
        msg = "成功"
    except Exception as e:
        msg = str(e)
    return jsonify({"msg": msg})
