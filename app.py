from flask import Flask, render_template, request, flash, session, url_for, redirect
import os
from flask_sqlalchemy import SQLAlchemy

# 获取当前html和css的路径
from sqlalchemy import and_

BASE_DIR = os.getcwd()
templates_dir = os.path.join(BASE_DIR, 'templates')
static_dir = os.path.join(BASE_DIR, 'static')

# 生成文本数据库
app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite') + '?check_same_thread=False' + '?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
# 定义数据库key
secret_key = os.urandom(24)
app.secret_key = secret_key

db = SQLAlchemy(app=app)


class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __repr__(self) :
        return '<User %r>' % self.user_name


# 添加数据库数据
@app.before_first_request
class create_db() :
    db.drop_all()
    db.create_all()

    admin = User(user_name='admin', password='root')
    db.session.add(admin)

    guestes = [User(user_name='123', password='123'),
               User(user_name='321', password='321'),
               User(user_name='234', password='234')]
    db.session.add_all(guestes)
    db.session.commit()


# 主页定义
@app.route('/')
def login1() :
    return render_template('./html/login1.html')


@app.route('/index')
def index() :
    return render_template('./html/index.html')


# 登录验证账户密码是否正确
def valid_login(user_name, password):
    user = User.query.filter(and_(User.user_name == user_name, User.password == password)).first()
    if user :
        return True
    else :
        return False


# 登录跳转的POST请求定义
@app.route('/index', methods=['GET', 'POST'])
def login() :
    error = None
    if request.method == 'POST':
        if valid_login(request.form['user_name'], request.form['password']) :
            flash('成功登陆')
            session['user_name'] = request.form.get('user_name')
            return redirect(url_for('index'))
        else:
            error = '错误的用户名和密码！'

    return render_template('./html/login1.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
