from flask import session, redirect, url_for, g
from functools import wraps

import config


def login_required(func):
    """登录验证装饰器"""
    @wraps(func)
    def inner(*args, **kwargs):
        if config.CMS_USER_SESSION in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner


def premission_required(premission):
    """权限验证"""
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if g.cms_user.has_premissions(premission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.profile'))

        return inner
    return outer
