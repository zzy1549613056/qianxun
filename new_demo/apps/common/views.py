from flask import Blueprint
import json,datetime,time,base64,hmac
from hashlib import sha1 as sha

common_bp = Blueprint('common',__name__,url_prefix='/common')

@common_bp.route('/aliyun')
def aliyun():
    accessKeyId = 'LTAIMhcythNhohBA'
    accessKeySecret = 'wgwVsNf8ryzsIPk65XZHHyZWGJeGnR'
    host = 'http://flaskdemo.oss-cn-hangzhou.aliyuncs.com';
    expire_time = 30
    upload_dir = 'banner/'
    now = int(time.time())
    expire_syncpoint = now + expire_time
    gmt = datetime.datetime.fromtimestamp(expire_syncpoint).isoformat()
    gmt += 'Z'
    expire = gmt
    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    # policy_encode = base64.encodestring(policy)
    #print(policy)
    policy_encode = base64.b64encode(policy.encode())
    #print(policy_encode)
    h = hmac.new(accessKeySecret.encode(), policy_encode, sha)
    sign_result = base64.encodebytes(h.digest()).strip()
    token_dict = {}
    token_dict['accessid'] = accessKeyId
    token_dict['host'] = host
    token_dict['policy'] = policy_encode.decode()
    token_dict['signature'] = sign_result.decode()
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    print(token_dict)
    result = json.dumps(token_dict)
    return result
