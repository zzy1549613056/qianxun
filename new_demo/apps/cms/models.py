from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSUser(db.Model):
    __tablename__ = "cms_user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return  self._password

    @password.setter
    def password(self,value):
        self._password = generate_password_hash(value)

    def check_password(self,value):
        return check_password_hash(self.password,value)
