import os
import time

from apps.flask_pj.model import *
from datetime import datetime,date,timedelta

# root_dir = os.path.dirname(os.path.abspath('.'))
# print(root_dir)
# with open(root_dir + "\\getSpeech\\words.tsv", "r", encoding="utf-8") as f:
#     content = f.read()
#     datas = content.split("\n\n")[:-1]
#     for data in datas:
#         info = data.split("\t")
#         print(info)
#         word_writing = info[0]
#         word_symbol = info[2]
#         word_pronunciation = str(datas.index(data)) + word_writing + ".mp3"
#         word_explanation = info[1]
#         if word_explanation[-1:] == "\n":
#             word_explanation = word_explanation[:-1]
#         word_example = info[3] + info[4] + "\n" + info[5] + info[6]
#     print(len(datas))

path='C:\\Users\\情若炎兮\\Desktop\\实习APP\\group1\\flask_app\\flask_pj\\apps\\static\\pronunciation\\'

# 获取该目录下所有文件，存入列表中
fileList = os.listdir(path)

n = 0
for i in fileList:
    # 设置旧文件名（就是路径+文件名）
    oldname = path + os.sep + fileList[n]  # os.sep添加系统分隔符
    # 设置新文件名
    newname = oldname.split('.')[0]+oldname.split('.')[1]+'.'+oldname.split('.')[2]

    os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
    print(oldname, '======>', newname)

    n += 1
print(n)
#     # word_id = db.UUIDField(primary_key=True, default=uuid.uuid4())
#     # writing = db.StringField(required=True, unique=True)
#     # symbol = db.StringField(required=True)
#     # pronunciation = db.StringField(required=True)
#     # explanation = db.StringField(required=True)
#     # example = db.StringField(required=True)
#
#
#
# abb = "123456"
# print(abb[:10])

# day = date.today()
# now = datetime.now()
# print(now)
# now = str(now).split(".")[0]
# data = datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S')
# delta = timedelta(days=5)  # days可以为正负数，当为负数时，n_days_after 与n_days_forward 的值与正数时相反；
# n_days_after = now + delta  # 当前日期推迟n天之后的时间
# n_days_forward = now - delta  # 当前日期向前推n天的时间
# print(datetime.now().strftime("%Y-%m-%d"))
# print(("当前日期：{}").format(day))
# t1="{}".format(day)
# t2="2020-05-05"
# time1 = t1.split("-")
# time2 = t2.split("-")
# date1 = date(int(time1[0]), int(time1[1]), int(time1[2]))
# date2 = date(int(time2[0]), int(time2[1]), int(time2[2]))
# print(date1.__sub__(date2).days)
