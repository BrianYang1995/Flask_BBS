# coding=utf-8

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, EqualTo, Regexp, ValidationError, InputRequired

from utils import mcache


class SignUpForm(Form):
    """注册"""
    telephone = StringField(validators=[Regexp(r'^1[345789]\d{9}$', message='手机号格式错误')])
    sms_captcha = StringField(validators=[Regexp(r'^[a-zA-Z0-9]{4}$')])
    username = StringField(validators=[Regexp(r'\w{2,20}')])
    password = StringField(validators=[Regexp(r'\w{6,20}')])
    password2 = StringField(validators=[EqualTo('password')])
    img_captcha = StringField(validators=[Regexp(r'[a-zA-Z0-9]{4}')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data.lower()
        telephone = self.telephone.data or 'w'
        m_captcha = mcache.get(telephone)

        if m_captcha != sms_captcha:
            raise ValidationError('短信验证码错误')
        mcache.delete(telephone)

    def validate_img_captcha(self, field):
        captcha = field.data
        if captcha:
            m_captcha = mcache.get(field.data.lower())

            if not m_captcha:
                raise ValidationError('验证码错误')
        else:
            raise ValidationError('验证码错误')

        mcache.delete(field.data)

    def get_error(self):

        return self.errors.popitem()[1][0]


class SignInForm(Form):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message='手机号格式错误')])
    password = StringField(validators=[Length(6, 20, message='密码长度错误')])
    remember = StringField()

    def get_error(self):
        return self.errors.popitem()[1][0]


class AddNewPostForm(Form):
    title = StringField(validators=[Length(1, 100), InputRequired(message='请输入帖子标题')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
    content = StringField(validators=[InputRequired(message='请输入帖子内容')])

    def get_error(self):
        return self.errors.popitem()[1][0]


class AddComment(Form):
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子')])
    content = StringField(validators=[Length(1, 1000, message='评论超长'), InputRequired('评论为空')])

    def get_error(self):
        return self.errors.popitem()[1][0]
