from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,InputRequired,regexp

class MessageForm(Form):
    name = StringField(validators=[Length(2, 11, message="姓名2-15字符")])
    tel = StringField(validators=[regexp(r'1[3456789]\d{9}', message="请输入正确电话号码")])
    email = StringField()
    kind = IntegerField()
    question = StringField(validators=[InputRequired(message='请输入咨询内容'),Length(0,200,message='咨询内容不超过200字符')])