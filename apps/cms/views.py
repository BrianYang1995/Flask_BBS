# coding=utf-8

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    url_for,
    redirect,
    session,
    g,
    jsonify
)

from flask_mail import Message
from flask_paginate import Pagination, get_parameter

import config

from .forms import (LoginForm,
                    ResetPWDForm,
                    CaptchaEmail,
                    CheckCaptchs,
                    AddBannerForm,
                    UpdateBannerForm,
                    AddBoardForm,
                    UpdateBoardForm
)
from .models import CMSUser, CMSPermission
from .decorators import login_required, premission_required
from exts import db, mail
from utils import restful, mcache
from utils.captcha import get_captcha
import tasks

from apps.models import (
    Banners,
    Boards,
    Comments,
    Posts,
    HighLightPosts
)

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    """获取主页"""
    return render_template('cms/index.html')


@bp.route('/logout/')
@login_required
def logout():
    """注销"""
    session.clear()
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    """获取用户信息"""
    return render_template('cms/profile.html')


@bp.route('/banners/')
@login_required
def banners():
    """轮播图管理"""
    banners = Banners.query.order_by(Banners.priority.desc()).all()
    return render_template('cms/banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    """添加轮播图"""
    form = AddBannerForm(request.form)

    if not form.validate():
        return restful.params_error(form.get_error())

    name = form.name.data
    img_url = form.img_url.data
    link_url = form.link_url.data
    priority = form.priority.data

    banner = Banners(name=name, img_url=img_url, link_url=link_url, priority=priority)
    db.session.add(banner)
    db.session.commit()
    return restful.success()


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    """修改轮播图"""
    form = UpdateBannerForm(request.form)

    if not form.validate():
        return restful.params_error(form.get_error())

    name = form.name.data
    img_url = form.img_url.data
    link_url = form.link_url.data
    banner_id = form.banner_id.data
    priority = form.priority.data

    banner = Banners.query.get(banner_id)
    if not banner:
        return restful.params_error('轮播图id不存在')

    banner.name = name
    banner.img_url = img_url
    banner.link_url = link_url
    banner.priority = priority
    db.session.commit()
    return restful.success()


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    """删除轮播图"""
    banner_id = request.form.get('banner_id')

    if not banner_id:
        return restful.params_error('参数错误')

    banner = Banners.query.get(banner_id)
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@premission_required(CMSPermission.COMMENTER)
def comments():
    """评论管理"""
    return render_template('cms/comments.html')


@bp.route('/boards/')
@login_required
@premission_required(CMSPermission.BORDER)
def boards():
    """版块管理"""
    boards = Boards.query.all()

    context = {
        'boards': boards,
    }
    return render_template('cms/boards.html', **context)


@bp.route('/aboards/', methods=['POST'])
@login_required
@premission_required(CMSPermission.BORDER)
def aboards():
    """添加版块"""
    form = AddBoardForm(request.form)

    if not form.validate():
        return restful.params_error(form.get_error())

    board = Boards(name=form.name.data)
    db.session.add(board)
    db.session.commit()
    return restful.success()


@bp.route('/uboards/', methods=['POST'])
@login_required
@premission_required(CMSPermission.BORDER)
def uboards():
    """更新版块"""
    form = UpdateBoardForm(request.form)

    if not form.validate():
        return restful.params_error(form.get_error())

    board_id = form.id.data
    board_name = form.name.data
    print(board_name)

    board = Boards.query.get(board_id)
    if not board:
        return restful.params_error('板块不存在')

    board.name = board_name
    print(board.name)
    db.session.commit()
    return restful.success()


@bp.route('/dboards/', methods=['POST'])
@login_required
@premission_required(CMSPermission.BORDER)
def dboards():
    """删除板块"""
    board_id = request.form.get('id')
    if not board_id:
        return restful.params_error('没有板块id')

    board = Boards.query.get(board_id)
    if not board:
        return restful.params_error('板块不存在')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/posts/')
@login_required
@premission_required(CMSPermission.POSTER)
def posts():
    """帖子管理"""
    page = request.args.get(get_parameter(), type=int, default=1)

    start = (page - 1) * config.POST_PER_PAGE
    end = start + config.POST_PER_PAGE
    post_query = Posts.query.order_by(Posts.create_time.desc())
    paginator = Pagination(bs_version=3, page=page, total=post_query.count(), per_page=config.POST_PER_PAGE, outer_window=0)
    posts_list = post_query.slice(start, end)

    context = {
        'posts': posts_list,
        'pagination': paginator
    }
    return render_template('cms/posts.html', **context)


@bp.route('/mark/', methods=['POST'])
@login_required
@premission_required(CMSPermission.POSTER)
def mark():
    """标星"""
    post_id = request.form.get('post_id')
    post = Posts.query.get(post_id)

    if not post:
        return restful.params_error('帖子id错误')

    mark_ = HighLightPosts.query.filter(HighLightPosts.post == post).first()

    if mark_:
        return restful.success('已为该帖子加星')

    mark = HighLightPosts(post=post)

    db.session.add(mark)
    db.session.commit()
    return restful.success()


@bp.route('/umark/', methods=['POST'])
@login_required
@premission_required(CMSPermission.POSTER)
def umark():
    """取消标星"""
    post_id = request.form.get('post_id')
    post = Posts.query.get(post_id)

    if not post:
        return restful.params_error('帖子id错误')

    mark = HighLightPosts.query.filter(HighLightPosts.post == post).first()
    if not mark:
        return restful.success('已为该帖子取消加星')

    db.session.delete(mark)
    db.session.commit()
    return restful.success()


@bp.route('/cmsroles/')
@login_required
@premission_required(CMSPermission.ADMINER)
def cmsroles():
    """CMS组管理"""
    return render_template('cms/cmsroles.html')


@bp.route('/cmsusers/')
@login_required
@premission_required(CMSPermission.CMSUSER)
def cmsusers():
    """CMS用户管理"""
    return render_template('cms/cmsusers.html')


@bp.route('/fusers/')
@login_required
@premission_required(CMSPermission.FRONTUSER)
def fusers():
    """用户管理"""
    return render_template('cms/fusers.html')


@bp.route('/captcha_email/')
def captcha_email():
    """发送邮件"""
    form = CaptchaEmail(request.args)
    if not form.validate():
        return restful.params_error(form.get_error())

    email = form.email.data
    captcha = get_captcha()
    print(captcha)
    tasks.send_email.delay('XPYTHONX论坛', [email], '您的验证码是  <a href> %s </a>' % captcha)
    mcache.set(email, captcha)

    # message = Message('XPYTHONX论坛', recipients=[email], html='您的验证码是  <a href> %s </a>' % captcha)
    # try:
    #     mail.send(message)
    #     mcache.set(email, captcha)
    # except:
    #     return restful.server_error()
    return restful.success('发送成功')


class LoginView(views.MethodView):
    """登录"""
    def get(self, message=None, email=None):
        return render_template('cms/login.html', message=message, email=email)

    def post(self):
        form = LoginForm(request.form)
        email = form.email.data
        if form.validate():
            password = form.password.data
            remember = form.remember.data

            # 验证用户和密码
            user = CMSUser.query.filter_by(email=email).first()

            if user and user.check_password(password):
                session[config.CMS_USER_SESSION] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='用户名或密码错误', email=email)
        else:
            message = form.errors.popitem()[1][0]
            return self.get(message, email)


class ResetPWDView(views.MethodView):
    """修改密码"""
    decorators = [login_required, ]

    def get(self):
        return render_template('cms/reset_pwd.html')

    def post(self):
        form = ResetPWDForm(request.form)

        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user

            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.add(user)
                db.session.commit()
                return jsonify({'code': 200, 'message': ''})
            else:
                return jsonify({'code': 400, 'message': '旧密码错误'})
        else:
            error = form.get_error()
            return jsonify({'code': 400, 'message': error})


class ResetEmailView(views.MethodView):
    """修改邮箱"""
    decorators = [login_required,]

    def get(self):
        return render_template('cms/resetemail.html')

    def post(self):
        form = CheckCaptchs(request.form)
        if form.validate():
            email = form.email.data
            user = g.cms_user
            user.email = email
            db.session.add(user)
            try:
                db.session.commit()
                mcache.delete(email)
            except:
                return restful.server_error()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPWDView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
