from flask_mongoengine import MongoEngine

# 定义 MongoEngine
db = MongoEngine()


class User(db.Document):
    email = db.StringField(required=True)
    username = db.StringField(required=True, max_length=128, unique=True)
    password = db.StringField(required=True)

    def __repr__(self):
        return 'User(email="{}", username="{}")'.format(self.username, self.password)
