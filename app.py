from flask import Flask
from flask_wtf import CSRFProtect
from apps.cms import bp as cms_bp
from apps.commons import bp as commons_bp
from apps.frants import bp as frants_bp
from apps.ueditor import bp as ueditor_bp
from exts import db, mail, alidayu
import config


def bbs_init():
    """初始化app"""
    bbs = Flask(__name__)

    bbs.config.from_object(config)

    db.init_app(bbs)
    mail.init_app(bbs)
    alidayu.init_app(bbs)

    bbs.register_blueprint(cms_bp)
    bbs.register_blueprint(commons_bp)
    bbs.register_blueprint(frants_bp)
    bbs.register_blueprint(ueditor_bp)

    CSRFProtect(bbs)
    return bbs


app = bbs_init()
if __name__ == '__main__':

    app.run()
