import random
from flask import request
from qiniu import Auth, put_file, etag, put_data
import qiniu.config

from apps.article.models import Article_type
from apps.user.models import User


def upload_qiniu(filestorage):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '1fXvG9wkbN7AgRUG6usHDcRP5Bb85apcovRAIITP'
    secret_key = 'Aqf1lPAmUG72EdZJ7PxKtWHfWDYNdUycZP1TaAIN'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'myblog202006'
    # 上传后保存的文件名
    filename = filestorage.filename
    ran = random.randint(1, 1000)
    suffix = filename.rsplit('.')[-1]
    key = filename.rsplit('.')[0] + '_' + str(ran) + '.' + suffix
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, filestorage.read())
    return ret, info


def user_type():
    # 获取文章分类
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = request.cookies.get('uid',None)
    if user_id:
        user = User.query.get(user_id)
    return user, types
