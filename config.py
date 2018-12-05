import os
# 开启DEBUG模式
DEBUG = True

# 工程密钥
SECRET_KEY = b'\x98|\xad\x85\xb8\xc2\xad{\x9f\xa3>g\xb4;\xfc(\x0f1\xf3rT\xcb\xe13'

# Mysql数据库
HOST = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'Yang-9110'
DB_NAME = 'BBS'

DB_URI = 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{database}?charset=utf8'.format(
    user=USERNAME, pwd=PASSWORD, host=HOST, port=PORT, database=DB_NAME
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# CMSsession Key
CMS_USER_SESSION = 'FAJKLNFLA'
FRONT_USER_SESSION = 'FALNKLEEI384KJLAN'

# Send E-mail
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USERNAME = 'yangz_forwork@163.com'
MAIL_PASSWORD = 'yang9110'
MAIL_DEFAULT_SENDER = 'yangz_forwork@163.com'

# Captcha 位数
CAPTCHA_NUM = 6

# 阿里大于短信
ACCESS_KEY_ID = "LTAI6orYrhcZj2EW"
ACCESS_KEY_SECRET = "ocGrKDPqJ1lnRpRySivehoyCVcdCVi"
SIGN_NAME = 'xpythonx论坛'
TEMPLATE_CODE = 'SMS_151996861'

# 七牛
QINIU_ACCESS_KEY = 'JNXWnfjPbIibGFEIVYKddUgvI0cLBEVwWFxRxZPk'
QINIU_SECRET_KEY = '_XvtKMz-cQqdXDGPoMC68sFbwAxTvv6DYgxI_w_4'
QINIU_BUCKET = 'xpythonx-bbs'

# Ueditor
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET
UEDITOR_QINIU_DOMAIN = "http://s.xpythonx.com/"

# flask-paginate
PER_PAGE = 12
POST_PER_PAGE = 15

# celery
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'