# coding=utf-8

from exts import db

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSPermission(object):
    """CMS用户对应的二进制码"""
    # 全部权限
    ALL_PERMISSION = 0b11111111
    # 访问者
    VISITOR =        0b00000001
    # 管理帖子
    POSTER =         0b00000010
    # 管理评论
    COMMENTER =      0b00000100
    # 管理版块
    BORDER =         0b00001000
    # 管理前台用户
    FRONTUSER =      0b00010000
    # 管理后台
    CMSUSER =        0b00100000
    # 管理员
    ADMINER =        0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    premissions = db.Column(db.Integer, default=CMSPermission.VISITOR)

    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')


class CMSUser(db.Model):
    __tablename__ = 'cms_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, row_password):
        self._password = generate_password_hash(row_password)

    def check_password(self, row_password):
        result = check_password_hash(self.password, row_password)
        return result

    @property
    def premissions(self):
        """查看权限"""
        if not self.roles:
            return 0

        roles = self.roles
        all_premissions = 0
        for role in roles:
            premission = role.premissions
            all_premissions |= premission
        return all_premissions

    def has_premissions(self, premissions):
        return premissions & self.premissions == premissions

    @property
    def is_developer(self):
        return self.has_premissions(CMSPermission.ALL_PERMISSION)


