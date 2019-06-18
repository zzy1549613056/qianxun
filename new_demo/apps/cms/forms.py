from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,EqualTo,Email,InputRequired,regexp


class LoginForm(Form):
    username = StringField(validators=[Length(3,11,message="用户名3-12字符")])
    password = StringField(validators=[Length(3,12,message="密码3-12字符")])
    remember = IntegerField()

class AddbannerForm(Form):
    name = StringField(validators=[InputRequired(message="请输入图片名称")])
    img_url = StringField(validators=[InputRequired(message="请输入图片链接")])
    link_url = StringField(validators=[InputRequired(message="请输入图片指向链接")])
    weight = IntegerField(validators=[InputRequired(message="请输入图片优先级")])

class UpdateBannerForm(AddbannerForm):
    id = IntegerField(validators=[InputRequired(message="请求无效")])


class AddboardForm(Form):
    name = StringField(validators=[InputRequired(message='请输入版块名'),Length(2,15,message='名称在2-15字符间')])


class PostingsForm(Form):
    title = StringField(validators=[InputRequired(message='缺少标题')])
    content = StringField(validators=[InputRequired(message='缺少内容')])
    board_id = IntegerField(validators=[InputRequired(message='缺少版块')])


