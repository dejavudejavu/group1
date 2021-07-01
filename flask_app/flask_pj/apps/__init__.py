import os
from flask import Flask
from .flask_pj import init_blue_print,User
from .utils import config_log
from flask_pj.config import config
from flask_mongoengine import MongoEngine
import sys
# sys.path.append("flask_pj/model")
# import model

db = MongoEngine()

def create_app():
    config_log()
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config.get(env))
    init_blue_print(app)
    # 通过MONGODB_SETTINGS配置MongoEngine
    app.config['MONGODB_SETTINGS'] = {
        'db': 'hello',
        'host': '159.75.23.139',
        'port': 27017,
        'connect': True
    }

    db.init_app(app)

    return app
