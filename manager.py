from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from exts import db
from app import app
from apps.cms import models
from apps.cms.models import CMSUser, CMSRole, CMSPermission
from apps.frants.models import User
from apps import models

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '-password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    """创建CMS用户"""
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('创建CMS用户成功')


@manager.command
def create_role():
    """创建角色"""
    # 访问者
    visitor = CMSRole(name='访问者', desc='访问，修改个人信息')
    visitor.premissions = CMSPermission.VISITOR

    # 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    operitor = CMSRole(name='运营人员', desc='修改个人个人信息，管理帖子，管理评论，管理前台用户')
    operitor.premissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    # 管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员', desc='拥有管理员权限')
    admin.premissions = CMSPermission.VISITOR | CMSPermission.FRONTUSER | CMSPermission.COMMENTER | CMSPermission.POSTER | CMSPermission.BORDER | CMSPermission.CMSUSER | CMSPermission.ADMINER

    # 开发者
    developer = CMSRole(name='开发者', desc='拥有开发相关权限')
    developer.premissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operitor, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_role_to_user(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    role = CMSRole.query.filter_by(name=name).first()
    if not user:
        return '邮箱错误'
    if not role:
        return '角色错误'

    role.users.append(user)
    db.session.commit()


@manager.option('-e', '--email', dest='email')
def is_developer(email):
    user = CMSUser.query.filter_by(email=email).first()
    if user.is_developer:
        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者权限！')


@manager.command
def create_test_post():
    author = User.query.first()
    board = models.Boards.query.first()
    for i in range(200):
        title = '测试 %d' % i
        content = '测试 %d' % i

        post = models.Posts(title=title, content=content)
        post.author = author
        post.board = board

        db.session.add(post)
        db.session.commit()

    print('生成测试数据完成')


@manager.option('-n', '--name', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-t', '--telephone', dest='telephone')
def create_user(username, password, telephone):
    user = User(username=username, password=password, telephone=telephone)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
