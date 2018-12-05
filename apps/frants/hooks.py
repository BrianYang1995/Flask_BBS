from .views import bp, render_template
import config
from flask import session, g
from .models import User


@bp.before_request
def before_request_func():
    if config.FRONT_USER_SESSION in session:
        user_id = session[config.FRONT_USER_SESSION]
        user = User.query.get(user_id)
        if user:
            g.user = user


@bp.errorhandler(404)
def error_404():
    return render_template('front/404.html')
