from flask import session, g

import config

from .models import CMSUser, CMSPermission
from .views import bp


@bp.before_request
def before_request_func():
    user_id = session.get(config.CMS_USER_SESSION)
    if user_id:
        user = CMSUser.query.get(user_id)
        g.cms_user = user


@bp.context_processor
def context_processor_func():
    return {'premission': CMSPermission}