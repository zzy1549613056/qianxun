from flask import (
    Blueprint,
    request,
    jsonify,
    url_for,
    send_from_directory,
    current_app as app
)
import json
import re
import string
import time
import hashlib
import random
import base64
import sys
import os
from urllib import parse
import oss2
from io import BytesIO


# text,img = captcha.get_captcha()
# auth = oss2.Auth('LTAIMhcythNhohBA', 'wgwVsNf8ryzsIPk65XZHHyZWGJeGnR')
# bucket = oss2.Bucket(auth,'http://oss-cn-hangzhou.aliyuncs.com','flaskdemo')
# out = BytesIO()
# img.save(out, 'jpeg')
# out.seek(0)
# res = bucket.put_object('2.jpeg',out)
# print(res.status)

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'images')
UEDITOR_UPLOAD_TO_ALIYUN = True
UEDITOR_ALIYUN_ACCESS_KEY = "LTAIMhcythNhohBA"
UEDITOR_ALIYUN_SECRET_KEY = "wgwVsNf8ryzsIPk65XZHHyZWGJeGnR"
UEDITOR_ALIYUN_BUCKET_NAME = "flaskdemo"
UEDITOR_ALIYUN_DOMAIN = "http://oss-cn-hangzhou.aliyuncs.com"
UEDITOR_ALIYUN_OUTPUT = "https://flaskdemo.oss-cn-hangzhou.aliyuncs.com/ueditor/"

ue_bp = Blueprint('ueditor',__name__,url_prefix='/ueditor')

@ue_bp.before_app_first_request
def before_first_request():
    if UEDITOR_UPLOAD_PATH and not os.path.exists(UEDITOR_UPLOAD_PATH):
        os.mkdir(UEDITOR_UPLOAD_PATH)
    csrf = app.extensions.get('csrf')
    if csrf:
        csrf.exempt(upload)


def _random_filename(rawfilename):
    letters = string.ascii_letters
    random_filename = str(time.time()) + "".join(random.sample(letters,5))
    filename = hashlib.md5(random_filename.encode('utf-8')).hexdigest()
    subffix = os.path.splitext(rawfilename)[-1]
    return filename + subffix


@ue_bp.route('/upload/',methods=['GET','POST'])
def upload():
    action = request.args.get('action')
    result = {}
    if action == 'config':
        config_path = os.path.join(ue_bp.static_folder or app.static_folder,'ueditor','config.json')
        with open(config_path,'r',encoding='utf-8') as fp:
            result = json.loads(re.sub(r'\/\*.*\*\/','',fp.read()))

    elif action in ['uploadimage','uploadvideo','uploadfile']:
        image = request.files.get("upfile")
        filename = image.filename
        save_filename = _random_filename(filename)
        result = {
            'state': '',
            'url': '',
            'title': '',
            'original': ''
        }
        if UEDITOR_UPLOAD_TO_ALIYUN:
            if not sys.modules.get('oss2'):
                raise RuntimeError('没有导入阿里云模块！')
            buffer = BytesIO()
            image.save(buffer)
            buffer.seek(0)
            auth = oss2.Auth(UEDITOR_ALIYUN_ACCESS_KEY, UEDITOR_ALIYUN_SECRET_KEY)
            bucket = oss2.Bucket(auth, UEDITOR_ALIYUN_DOMAIN, UEDITOR_ALIYUN_BUCKET_NAME)
            res = bucket.put_object('ueditor/' + save_filename, buffer)
            print(res.status)
            if res.status == 200:
                result['state'] = "SUCCESS"
                result['url'] = UEDITOR_ALIYUN_OUTPUT + save_filename + "?x-oss-process=style/original_format"
                result['title'] = save_filename
                result['original'] = image.filename
        else:
            image.save(os.path.join(UEDITOR_UPLOAD_PATH, save_filename))
            result['state'] = "SUCCESS"
            result['url'] = url_for('ueditor.files',filename=save_filename)
            result['title'] = save_filename,
            result['original'] = image.filename

    elif action == 'uploadscrawl':
        base64data = request.form.get("upfile")
        img = base64.b64decode(base64data)
        filename = _random_filename('xx.png')
        filepath = os.path.join(UEDITOR_UPLOAD_PATH,filename)
        with open(filepath,'wb') as fp:
            fp.write(img)
        result = {
            "state": "SUCCESS",
            "url": url_for('ueditor.files',filename=filename),
            "title": filename,
            "original": filename
        }
    return jsonify(result)

@ue_bp.route('/files/<filename>/')
def files(filename):
    return send_from_directory(UEDITOR_UPLOAD_PATH,filename)
