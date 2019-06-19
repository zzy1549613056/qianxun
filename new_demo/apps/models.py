from exts import db
from datetime import  datetime
from jieba.analyse.analyzer import ChineseAnalyzer

class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    img_url = db.Column(db.String(255),nullable=False)
    link_url = db.Column(db.String(255),nullable=False)
    weight = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)

class PostingsModel(db.Model):
    __tablename__ = 'posting'
    __searchable__ = ['title', 'content']
    __analyzer__ = ChineseAnalyzer()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))

class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    postings = db.relationship('PostingsModel',backref='board')

class MessageModel(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(11),nullable=False)
    email = db.Column(db.String(50),nullable=True)
    kind = db.Column(db.Integer,nullable=False)
    question = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

# class TestModel(db.Model):
#     __tablename__ = 'test'
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)