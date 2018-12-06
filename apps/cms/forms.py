# coding=utf-8

from wtforms import Form, StringField, IntegerField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from flask import g

from utils import mcache


class LoginForm(Form):
    """登录验证"""
    email = StringField(validators=[Email(message='邮箱格式不正确'), InputRequired(message='请输入邮箱地址')])
    password = StringField(validators=[Length(6, 20, message='密码长度错误')])
    remember = IntegerField()


class ResetPWDForm(Form):
    """修改密码"""
    oldpwd = StringField(validators=[Length(6, 20, message='旧密码长度错误')])
    newpwd = StringField(validators=[Length(6, 20, message='新密码长度不够')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次密码不相等')])

    def get_error(self):
        errors = self.errors
        if 'oldpwd' in errors:
            return errors['oldpwd'][0]
        elif 'newpwd' in errors:
            return errors['newpwd'][0]
        elif 'newpwd2' in errors:
            return errors['newpwd2'][0]
        else:
            return


class CaptchaEmail(Form):
    """验证邮箱"""
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱地址')])

    def validate_email(self, field):
        email = field.data
        email_cache = mcache.get(email)
        if email_cache:
            raise ValidationError('请求过于频繁，请稍后再试')

    def get_error(self):
        return self.errors.popitem()[1][0]


class CheckCaptchs(Form):
    """验证验证码"""
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='未填入邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='验证码长度错误')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data

        cache_captcha = mcache.get(email)

        if cache_captcha:
            if captcha.lower() != cache_captcha.lower():
                raise ValidationError('验证码错误')
        else:
            raise ValidationError('验证码无效')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user

        if email == user.email:
            raise ValidationError('新邮箱与与旧邮箱相同')

    def get_error(self):
        return self.errors.popitem()[1][0]


class AddBannerForm(Form):
    """轮播图验证"""
    name = StringField(validators=[Length(1, 100), InputRequired(message='请填入标题')])
    img_url = StringField(validators=[Length(1, 200), InputRequired(message='请填入正确的地址')])
    link_url = StringField(validators=[Length(1, 200), InputRequired(message='请填入正确的地址')])
    priority = IntegerField(validators=[InputRequired(message='请输入权重')])

    def get_error(self):
        return self.errors.popitem()[1][0]


class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='缺少id')])


class AddBoardForm(Form):
    name = StringField(validators=[Length(1, 50), InputRequired(message='请输入板块名称')])

    def get_error(self):
        return self.errors.popitem()[1][0]


class UpdateBoardForm(AddBoardForm):
    id = IntegerField(validators=[InputRequired(message='缺少板块id')])

