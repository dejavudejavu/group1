后台打开方式：
1.安装依赖：终端进入flask_app\flask_pj这个目录下面，输入pip install -r requirements.txt
2.启动后台：同一个目录下python manage.py 8888
3.修改前端地址：app.js中的globalData中的baseUrl改成自己的内网地址，一定是内网地址
4.运行前端项目


|   |-- flask_app 	后台工程
|   |   `-- flask_pj
|   |       |-- __init__.py
|   |       |-- __pycache__
|   |       |   |-- __init__.cpython-39.pyc
|   |       |   `-- config.cpython-39.pyc
|   |       |-- apps
|   |       |   |-- __init__.py
|   |       |   |-- __pycache__
|   |       |   |   `-- __init__.cpython-39.pyc
|   |       |   |-- flask_pj
|   |       |   |   |-- __init__.py
|   |       |   |   |-- __pycache__
|   |       |   |   |   `-- __init__.cpython-39.pyc
|   |       |   |   |-- controller
|   |       |   |   |-- model	数据库模型
|   |       |   |   |-- templates	模板(本项目前后端分离，不采用)
|   |       |   |   `-- view	    视图
|   |       |   |-- logs
|   |       |   |-- static
|   |       |   `-- utils
|   |       |       |-- __init__.py
|   |       |       |-- __pycache__
|   |       |       |   |-- __init__.cpython-39.pyc
|   |       |       |   `-- constants.cpython-39.pyc
|   |       |       `-- constants.py
|   |       |-- config.py
|   |       |-- gconfig.py
|   |       |-- manage.py	开发环境启动入口
|   |       |-- requirements.txt
|   |       |-- startserver.sh
|   |       `-- wsgi.py	正式环境启动入口
|   `-- mini_program	小程序前端工程
|       |-- app.js
|       |-- app.json
|       |-- app.wxss
|       |-- miniprogram_npm	项目依赖
|       |-- package-lock.json
|       |-- package.json
|       |-- pages	（待增加）
|       |   |-- doHomework	记单词页面
|       |   |-- homepage	主界面
|       |   |-- chooseBook	选书页面
|       |   |-- clockIn	打卡页面
|       |   |-- myBook	我的图书页面
|       |   |-- myPlan	我的计划页面
|       |   |-- wordExplaination	单词解释页面
|       |   |-- index
|       |   |-- logs
|       |   `-- personal	个人中心页面
|       |-- project.config.json
|       |-- sitemap.json
|       `-- utils
|           `-- util.js

