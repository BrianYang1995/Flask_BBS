# coding=utf-8

from flask import redirect, url_for, session
import config
from functools import wraps


def login_required(func):
    """登录装饰器"""
    @wraps(func)
    def inner(*args, **kwargs):
        if config.FRONT_USER_SESSION in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('frants.signin'))

    return inner