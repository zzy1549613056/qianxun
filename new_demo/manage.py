from flask_script import Manager
from apps.models import PostingsModel,BoardModel,MessageModel,BannerModel
from apps.cms.models import CMSUser
from exts import app,db
import re
import requests
from math import ceil
import new_demo
manager = Manager(app)


@manager.command
def hello():
    print('hello world')

##sub的替换函数
# def add(m):
#     return 'http://www.hzbb315.com'+m.group(0)

@manager.command
def addModel():
    db.create_all()

@manager.command
def addCmsUser():
    user = CMSUser('root','root123','154961306@qq.com')
    db.session.add(user)
    db.session.commit()


@manager.command
def addPosting():
    count = 0
    url_index = 'http://www.hzbb315.com/news/index.html'
    url_news = 'http://www.hzbb315.com/news/index/p/'
    url_detail = 'http://www.hzbb315.com/news/detail/id/'
    r = requests.get(url_index).text
    page_match = re.search(r'共 (\d+) 条记录', r).group(1)
    if page_match:
        pages = ceil(int(page_match) / 20)
    else:
        print('获取页数失败')
        pages = 0
    print('共有' + str(pages) + '页')

    for page in range(pages):
        url = url_news + str(page + 1) + '.html'
        news_res = requests.get(url).text
        new_id_dict = re.findall(r'\<a href=\"\/news\/detail\/id\/(.*?)\"', news_res)
        for id in new_id_dict:
            url = url_detail + id
            detail_res = requests.get(url).text
            content_match = re.search(r'\<div class\=\"contentdetail\"\>(.*)\<p.*\<\/p\>\s*\<\/div\>', detail_res,
                                      flags=re.S)
            title_match = re.search(r'\<div class\=\"pname\"\>(.*?)\<\/div\>', detail_res, flags=re.S)
            if content_match:
                post = PostingsModel(title=title_match.group(1),content=re.sub(r'(?<!com)\/Upload\/image\/', lambda m:'http://www.hzbb315.com'+m.group(0), content_match.group(1)),board_id=6)
                db.session.add(post)
                db.session.commit()
                print(id)
                count += 1
            else:
                print('该页面为空')
    print(count)


if __name__ == '__main__':
    manager.run()



