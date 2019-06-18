from flask import Flask
from flask_wtf import CSRFProtect
import config
from apps.cms import models as cms_model
from apps.cms.views import cms_bp
from apps.front.views import front_bp
from apps.common.views import common_bp
from apps.ueditor.ueditor import ue_bp
from exts import db,mail,app
import re
import flask_whooshalchemyplus

# app = Flask(__name__)
app.config.from_object(config)

app.register_blueprint(front_bp)
app.register_blueprint(cms_bp)
app.register_blueprint(common_bp)
app.register_blueprint(ue_bp)

db.init_app(app)
mail.init_app(app)
CSRFProtect(app)
flask_whooshalchemyplus.init_app(app)


@app.template_filter('cut')
def cut(html):
    return re.sub(r'\<.*?\>|&nbsp;|\s', "", html,flags=re.S)

@app.template_filter('get_img')
def get_img(html):
    res = re.match(r'.*?\<img.*?src=\"(.*?)"', html,flags=re.S)
    if res:
        return res.group(1)
    else:
        return "/static/img/logo.png"

@app.template_filter('search_cut')
def searcha(html,key):
    res = re.search('([^\。\，\,]*'+key+'.*)',html,flags=re.I)
    if res:
        return res.group(1)[:50]
    else:
        return ''



# with app.app_context():
#     flask_whooshalchemyplus.index_all(app)
#初始化搜索索引时使用

# with app.app_context():
#     db.create_all()
#初始化创建数据库时使用

# with app.app_context():
#     user = cms_model.CMSUser('root','242501','123121')
#     db.session.add(user)
#     db.session.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5002)
    # app.run(host="0.0.0.0", port=5002, use_reloader=False)
