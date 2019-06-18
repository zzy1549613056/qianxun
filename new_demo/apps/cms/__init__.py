from .views import cms_bp
from flask import g,session
from .models import CMSUser

#上下文钩子函数，将用户信息填充到模版中
@cms_bp.context_processor
def my_context_processor():
    if hasattr(g,"cms_user"):
        return {
            'user':g.cms_user
        }
    return {
    }



@cms_bp.before_request
def my_before_request():
    id = session.get('cms_user_id')
    if id:
        user = CMSUser.query.get(id)
        if user:
            g.cms_user = user