from flask import Blueprint,render_template,request,views,redirect,url_for,session
from .forms import LoginForm,AddbannerForm,UpdateBannerForm,AddboardForm,PostingsForm
from .models import CMSUser
from ..models import BannerModel,PostingsModel,BoardModel,MessageModel
from .decorators import login_required
from exts import db
from utils import restful


cms_bp = Blueprint("cms",__name__,url_prefix='/cms')

@cms_bp.route('/')
@login_required
def index():
    return render_template('cms/base.html')


@cms_bp.route('/logout')
def logout():
    del session['cms_user_id']
    return redirect(url_for('cms.login'))

###########轮播图管理
@cms_bp.route('/banner_manage')
@login_required
def banner_manage():
    banners = BannerModel.query.order_by(-BannerModel.weight).all()
    return render_template('cms/banner_manage.html',banners=banners)

@cms_bp.route('/banner_delete',methods=['POST'])
@login_required
def banner_delete():
    id = request.form.get('id')
    if not id:
        return restful.params_error('id没输入')
    banner = BannerModel.query.get(id)
    if not banner:
        return restful.params_error('id错误或图片已经不存在')
    db.session.delete(banner)
    db.session.commit()
    return restful.success()

@cms_bp.route('/banner_add',methods=['POST'])
@login_required
def banner_add():
    form = AddbannerForm(request.form)
    if form.validate():
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        weight = form.weight.data
        banner = BannerModel(name=name, img_url=img_url, link_url=link_url, weight=weight)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        print(form.errors)
        errors = form.errors
        return restful.params_error(errors[list(errors.keys())[0]][0])

@cms_bp.route('/banner_update',methods=['POST'])
@login_required
def banner_update():
    form = UpdateBannerForm(request.form)
    if form.validate():
        id = form.id.data
        name = form.name.data
        img_url = form.img_url.data
        link_url = form.link_url.data
        weight = form.weight.data
        banner = BannerModel.query.get(id)
        banner.name = name
        banner.img_url = img_url
        banner.link_url = link_url
        banner.weight = weight
        db.session.commit()
        return restful.success()
    else:
        print(form.errors)
        errors = form.errors
        return restful.params_error(errors[list(errors.keys())[0]][0])

########版块管理
@cms_bp.route('/boards')
@login_required
def boards():
    boards = BoardModel.query.order_by(-BoardModel.create_time).all()
    return render_template('cms/boards.html',boards=boards)

@cms_bp.route('/boards_add',methods=['POST'])
@login_required
def boards_add():
    form = AddboardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        errors = form.errors
        return restful.params_error(errors[list(errors.keys())[0]][0])

@cms_bp.route('/boards_update', methods=['POST'])
@login_required
def boards_update():
   id = request.form.get('id')
   name = request.form.get('name')
   if len(name) <=20 :
       board = BoardModel.query.get(id)
       if not board:
           restful.params_error('请刷新页面后再尝试试')
       board.name = name
       db.session.commit()
       return restful.success()
   else:
       return restful.params_error('版块名小于20个字符')

@cms_bp.route('/boards_delete', methods=['POST'])
@login_required
def boards_delete():
    id = request.form.get('id')
    if not id:
        return restful.params_error('请刷新页面后再尝试试')
    board = BoardModel.query.get(id)
    if not board:
        return restful.params_error('请刷新页面后再尝试试')
    db.session.delete(board)
    db.session.commit()
    return restful.success()










###########发布咨询
@cms_bp.route('/postings',methods=['POST','GET'])
@login_required
def postings():
    if request.method == 'GET':
        boards = BoardModel.query.order_by(-BoardModel.create_time).all()
        return render_template('cms/postings.html',boards=boards)
    else:
        form = PostingsForm(request.form)
        if form.validate():
            board_id = form.board_id.data
            title = form.title.data
            content = form.content.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error('没有该版块')
            posting = PostingsModel(title=title,content=content,board_id=board_id)
            db.session.add(posting)
            db.session.commit()
            return restful.success()
        else:
            print(form.errors)
            errors = form.errors
            return restful.params_error(errors[list(errors.keys())[0]][0])


# 管理资讯
@cms_bp.route('/post_manage/')
@login_required
def post_manage():
    search = request.args.get('search')
    page = request.args.get('page',1,type=int)
    if search == 'board':
        paginate = PostingsModel.query.order_by(PostingsModel.board_id).paginate(page,per_page=5,error_out=False)
    else:
        paginate = PostingsModel.query.order_by(-PostingsModel.create_time).paginate(page,per_page=5,error_out=False)
    return render_template('cms/posting_manage.html',paginate=paginate)

@cms_bp.route('/post_delete',methods=['POST'])
@login_required
def post_delete():
    id = request.form.get('id')
    if not id:
        return restful.params_error('请刷新页面再尝试')
    post = PostingsModel.query.get(id)
    if not post:
        return restful.params_error('请刷新页面再尝试')
    db.session.delete(post)
    db.session.commit()
    return restful.success()


#用户咨询
@cms_bp.route('/message/')
@login_required
def message():
    search = request.args.get('search')
    page = request.args.get('page',1,type=int)
    if search == 'kind':
        paginate = MessageModel.query.order_by(MessageModel.kind).paginate(page,per_page=5,error_out=False)
    else:
        paginate = MessageModel.query.order_by(-MessageModel.create_time).paginate(page,per_page=5,error_out=False)
    return render_template('cms/message.html',paginate=paginate)

@cms_bp.route('/message_delete',methods=['POST'])
@login_required
def message_delete():
    id = request.form.get('id')
    if not id:
        return restful.params_error('请刷新页面再尝试')
    message = MessageModel.query.get(id)
    if not message:
        return restful.params_error('请刷新页面再尝试')
    db.session.delete(message)
    db.session.commit()
    return restful.success()







#cms登录
class LoginView(views.MethodView):
    def get(self,error=None):
        return render_template('cms/login.html', error=error)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter(CMSUser.username==username).first()
            if user and user.check_password(password):
                session['cms_user_id'] = user.id
                return redirect(url_for('cms.index'))
            return self.get(error='账号或密码错误')
        else:
            print(form.errors)
            errors = (''.join(form.errors['username']) if form.errors.get('username') else '')+' '+ \
                     (''.join(form.errors['password']) if form.errors.get('password') else '')
            return self.get(error=errors)



cms_bp.add_url_rule('/login',view_func=LoginView.as_view('login'))