from exts import db

from shortuuid import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 0
    SECRET = 3
    DOKNOW = 4


class User(db.Model):
    """前台用户"""
    __tablename__ = 'user'

    id = db.Column(db.String(50), primary_key=True, default=uuid)
    username = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(200))
    realname = db.Column(db.String(50))
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.DOKNOW)
    join_time = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.pop('password')

        super(User, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, password):
        return check_password_hash(self.password, password)