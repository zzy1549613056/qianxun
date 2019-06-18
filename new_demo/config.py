import os

DEBUG = True

##让jsonify返回的字符串支持中文
JSON_AS_ASCII = False

SECRET_KEY = "你猜你猜"

DIALECT = 'mysql'
DRIVE = 'pymysql'
USERNAME = 'root'
PASSWD = '242501'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'qianxun'


SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVE,USERNAME,PASSWD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
WHOOSH_BASE = os.path.dirname(__file__)+'/path/to/whoosh/base'


MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "465"
MAIL_USE_SSL = True
MAIL_USERNAME = "1549613056@qq.com"
MAIL_PASSWORD = "omibtdlpwmxxjaia"
MAIL_DEFAULT_SENDER = "1549613056@qq.com"