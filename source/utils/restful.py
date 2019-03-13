from flask import jsonify


class HttpCode(object):
    ok = 200
    unauthorerror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message or '', 'data': data or []})


def success(message=None, data=None):
    return restful_result(HttpCode.ok, message, data)


def unauth_error(message=None, data=None):
    return restful_result(HttpCode.unauthorerror, message or '权限不足', data)


def params_error(message=None, data=None):
    return restful_result(HttpCode.paramserror, message or '参数错误', data)


def server_error(message=None, data=None):
    return restful_result(HttpCode.servererror, message or '服务器错误', data)

























