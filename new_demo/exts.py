from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask

#将app分离出来，以便在蓝图中使用
app = Flask(__name__)
db = SQLAlchemy()
mail = Mail()



