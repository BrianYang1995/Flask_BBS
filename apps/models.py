from exts import db

from datetime import datetime


class Banners(db.Model):
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    link_url = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Boards(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    post_amount = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'))
    author_id = db.Column(db.String(50), db.ForeignKey('user.id'))

    board = db.relationship('Boards', backref='posts')
    author = db.relationship('User', backref='posts')


class HighLightPosts(db.Model):
    __tablename__ = 'highlightposts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    post = db.relationship('Posts', backref='highlight')


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(5000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    author_id = db.Column(db.String(50), db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    author = db.relationship('User', backref='comments')
    post = db.relationship('Posts', backref='comments')
