from flask import Blueprint, render_template, request, send_from_directory, current_app
from ..models import BannerModel, BoardModel, PostingsModel, MessageModel
from .forms import MessageForm
from utils import restful
from exts import db, mail,app
from flask_mail import Message
from concurrent.futures import ThreadPoolExecutor
import time

# 实现异步多线程操作
executor = ThreadPoolExecutor(1)

front_bp = Blueprint("front", __name__)

@front_bp.route('/favicon.ico')
def get_fav():
    print("favicon.ico请求")
    return ''


@front_bp.route('/')
def index():
    postings = PostingsModel.query.order_by(-PostingsModel.create_time).limit(4)
    banners = BannerModel.query.order_by(-BannerModel.weight).all()
    return render_template('front/index.html', banners=banners, postings=postings)


##############################产品与服务
@front_bp.route('/service/')
def service():
    return render_template('front/service.html')


##############################解决方案
@front_bp.route('/solution/<int:id>')
def solution(id):
    return render_template('front/solution.html', id=id)


##############################行业咨询
@front_bp.route('/info/')
def info():
    page = request.args.get('page', 1, type=int)
    current_board = request.args.get('id', 0, type=int)
    boards = BoardModel.query.order_by(-BoardModel.create_time).all()
    if current_board:
        paginate = PostingsModel.query.order_by(-PostingsModel.create_time).filter_by(board_id=current_board).paginate(
            page, per_page=5, error_out=True)
    else:
        paginate = PostingsModel.query.order_by(-PostingsModel.create_time).paginate(page, per_page=5, error_out=True)
    postings = paginate.items
    dict = {
        'paginate': paginate,
        'current_board': current_board,
        'boards': boards,
        'postings': postings

    }
    return render_template('front/info.html', **dict)


@front_bp.route('/info_detail/')
def info_detail():
    id = request.args.get('id')
    if id:
        posting = PostingsModel.query.get(id)
        return render_template('front/info_detail.html', posting=posting)
    else:
        return "404 not found "


####################################

##############################关于我们

def send_mail(name,tel,email,kind,question):
    kind_list = ['电商从业合规', '消费者维权', '知识产权保护', '其他']
    body = '姓名:' + name + '\n' + '电话:' + tel + '\n' + '邮件:' + email + '\n' + \
           '种类:' + kind_list[kind - 1] + '\n' + '问题:' + question
    with app.app_context():
        message = Message(subject='千寻科技问题咨询(自动邮件)', recipients=['1549613056@qq.com'], body=body)
        mail.send(message)
        print('邮件发送成功')



@front_bp.route('/about',methods=['GET','POST'])
def about():
    if request.method == 'GET':
        return render_template('front/about.html')
    else:
        form = MessageForm(request.form)
        if  form.validate():
            name = form.name.data
            tel = form.tel.data
            email = form.email.data
            kind = form.kind.data
            question = form.question.data
            executor.submit(send_mail,*[name,tel,email,kind,question])
            message = MessageModel(name=name,tel=tel,email=email,kind=kind,question=question)
            db.session.add(message)
            db.session.commit()
            return restful.success()
        else:
            errors = form.errors
            return restful.params_error(errors[list(errors.keys())[0]][0])


##############主页搜索
@front_bp.route('/search', methods=['POST'])
def search():
    content = request.form.get('content')
    search = content
    # print(content)
    results = PostingsModel.query.whoosh_search(content).all()
    return render_template('front/search_result.html', results=results,search=search)


# @front_bp.route("/download/<path:filename>")
# def downloader(filename):
#     return send_from_directory(front_bp.root_path,filename,as_attachment=True)


# def aa():
#     time.sleep(3)
#     print('hihi')
#     try:
#         with current_app.app_context():
#             message = Message('flask 异步A邮件',recipients=['1549613056@qq.com'],body='测试')
#     except Exception as e:
#         print(e)
#         print('error')
#     finally:
#         print('ok')
#         mail.send(message)

# 邮件服务测试
# @front_bp.route('/email')
# def send_email():
#     message = Message(subject='flask 邮件', recipients=['1549613056@qq.com'], body='测试')
#     mail.send(message)
#     return 'ok'