# coding=utf-8

from flask import Blueprint, request, make_response, jsonify

import json
from io import BytesIO
import qiniu

from .forms import MSMCaptchaForm
from exts import alidayu
from utils import restful
from utils.img_captcha import Captcha
from utils import mcache
import config
from tasks import send_sms


bp = Blueprint('commons', __name__, url_prefix='/c')


@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = MSMCaptchaForm(request.form)

    if not form.validate():
        return restful.params_error()
    telephone = form.telephone.data

    if mcache.get(telephone + '_'):
        return restful.params_error('请求过于频繁')

    captcha = Captcha.gene_text(4)
    mcache.set(telephone, captcha.lower(), 300)
    mcache.set(telephone + '_', 1, 60)

    send_sms.delay(telephone, captcha)
    # ret = alidayu.send_sms(telephone, key=captcha)
    # ret = json.loads(ret)

    return restful.success()


@bp.route('/imgcaptcha/')
def img_captcha():
    text, img = Captcha.gene_graph_captcha()
    out = BytesIO()
    img.save(out, 'png')
    out.seek(0)
    mcache.set(text.lower(), text.lower(), 300)
    response = make_response(out.read())
    response.content_type = 'image/png'
    return response


@bp.route('/uptoken/')
def uptoken():
    q = qiniu.Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    token = q.upload_token(config.QINIU_BUCKET)
    return jsonify({'uptoken': token})
