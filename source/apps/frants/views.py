# coding=utf-8

from flask import Blueprint, views, render_template, make_response, request, url_for, session, redirect, g, abort
from flask_paginate import Pagination, get_page_parameter


import config
from .models import User
from .forms import (
    SignUpForm,
    SignInForm,
    AddNewPostForm,
    AddComment
)

from utils import restful
from exts import db
from utils.safeutils import is_safe_url
from apps.models import (
    Banners,
    Boards,
    Posts,
    Comments,
    HighLightPosts
)

from .decorators import login_required

bp = Blueprint('frants', __name__)


@bp.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    board_id = request.args.get('bd', type=int, default=None)
    sort = request.args.get('sort', type=int, default=1)

    banners = Banners.query.order_by(Banners.priority.desc()).all()[:4]
    boards = Boards.query.all()

    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE

    if sort == 1:
        query_obj = Posts.query.order_by(Posts.create_time.desc())
    elif sort == 2:
        query_obj = db.session.query(Posts).outerjoin(HighLightPosts).order_by(HighLightPosts.create_time.desc(), Posts.create_time.desc())
    elif sort == 3:
        query_obj = db.session.query(Posts).outerjoin(Comments).group_by(Posts.id).order_by(db.func.count(Comments.id).desc(), Posts.create_time.desc())
    elif sort == 4:
        query_obj = Posts.query.order_by(Posts.create_time.desc())

    if board_id:
        board = Boards.query.get(board_id)
        if board:
            query_obj = query_obj.filter(Posts.board_id == board_id)

    total = query_obj.count()

    posts = query_obj.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, per_page=config.PER_PAGE, outer_window=0)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'board_id': board_id,
        'sort': sort
    }
    return render_template('front/index.html', **context)


@bp.route('/post_detail/<post_id>/')
def post_detail(post_id):
    """详情页"""
    post_id = post_id
    post = Posts.query.get(post_id)
    if not post:
        return abort(404)

    return render_template('front/post_detail.html', post=post)


class SignUpView(views.MethodView):
    """前台用户注册"""
    def get(self):
        refer = request.referrer

        if refer and refer != request.url and is_safe_url(refer):
            return_to = refer
        else:
            return_to = url_for('frants.index')

        return render_template('front/signup.html', return_to=return_to)

    def post(self):
        form = SignUpForm(request.form)

        if not form.validate():
            return restful.params_error(form.get_error())

        telephone = form.telephone.data
        password = form.password.data
        username = form.username.data
        user = User(username=username, password=password, telephone=telephone)
        db.session.add(user)
        try:
            db.session.commit()
            return restful.success()
        except:
            return restful.params_error()


class SignInView(views.MethodView):
    def get(self):
        referer = request.referrer
        if referer and is_safe_url(referer) and referer != request.url and referer != url_for('frants.signup'):
            return_to = referer
        else:
            return_to = '/'
        return render_template('front/signin.html', return_to=return_to)

    def post(self):
        form = SignInForm(request.form)

        if not form.validate():
            return restful.params_error(form.get_error())

        telephone = form.telephone.data
        password = form.password.data

        user = User.query.filter_by(telephone=telephone).first()
        if user and user.check_password(password):
            session[config.FRONT_USER_SESSION] = user.id
            if form.remember.data == '1':
                session.permanent = True
            return restful.success()
        else:
            return restful.params_error('用户名或密码错误')


@bp.route('/apost/', methods=['POST', 'GET'])
@login_required
def apost():
    if request.method == 'GET':
        boards = Boards.query.all()
        return render_template('front/apost.html', boards=boards)

    elif request.method == 'POST':
        # print(request.form)
        form = AddNewPostForm(request.form)

        if not form.validate():
            return restful.params_error(form.get_error())

        board_id = form.board_id.data
        board = Boards.query.get(board_id)

        if not board:
            return restful.params_error('板块不存在')

        title = form.title.data
        content = form.content.data

        post = Posts(title=title, content=content)
        post.board = board
        post.author = g.user
        db.session.add(post)
        db.session.commit()

        return restful.success()


@bp.route('/logout/')
@login_required
def logout():
    session.pop(config.FRONT_USER_SESSION)
    return redirect(url_for('frants.index'))


@bp.route('/acomment/', methods=['POST'])
@login_required
def acomment():
    """添加评论"""
    form = AddComment(request.form)

    if not form.validate():
        return restful.params_error(form.get_error())

    post_id = form.post_id.data

    post = Posts.query.get(post_id)
    if not post:
        return restful.params_error('帖子不存在')

    comment = Comments(content=form.content.data)
    comment.post = post
    comment.author = g.user
    db.session.add(comment)
    db.session.commit()
    return restful.success()


bp.add_url_rule('/signup/', view_func=SignUpView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignInView.as_view('signin'))
