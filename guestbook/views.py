# -*- coding: utf-8 -*-
"""
    :author: SharkCheung
    :copyright: © 2020 Shark Cheung <563049899@qq.com>
    :license: MIT, see LICENSE for more details.
"""
from io import BytesIO

from flask import flash, redirect, url_for, render_template, request, make_response, session

from guestbook import app, db
from guestbook.forms import HelloForm, LoginForm, RegForm
from guestbook.models import Message, User

from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
import functools

from guestbook.settings import FONT_DIR


def validate_picture():
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    # 图片大小130 x 50
    width = 130
    heighth = 50
    # 先生成一个新图片对象
    im = Image.new('RGB', (width, heighth), 'white')
    # 设置字体
    font = ImageFont.truetype(FONT_DIR, 40)
    # 创建draw对象
    draw = ImageDraw.Draw(im)
    str = ''
    # 输出每一个文字
    for item in range(4):
        text = random.choice(total)
        str += text
        draw.text((5 + random.randint(4, 7) + 20 * item, 5 + random.randint(3, 7)), text=text, fill='black', font=font)

    # 划几根干扰线
    for num in range(8):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, heighth / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(heighth / 2, heighth)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    # 模糊下,加个帅帅的滤镜～
    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page=None):
    per_page = request.args.get('per_page', 10, type=int)
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('留言发送成功！')
        return redirect(url_for('index'))

    messages = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=per_page)
    return render_template('index.html', form=form, messages=messages.items, pagination=messages)


@app.context_processor
def my_context_processor():
    status = session.get('status', '')
    user = session.get('user', '')
    return {'status': status, 'user': user}


def is_login(func):
    @functools.warps(func)
    def inner(*args, **kwargs):
        user = session.get('user')
        if not user:
            return redirect('login')
        return func(*args, **kwargs)

    return inner


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        userpass = form.userpass.data
        user = User(username=username, userpass=userpass)
        ret = user.check_login(username, userpass)
        if ret['code'] == 0:
            # db.session.add(message)
            # db.session.commit()
            session['status'] = 'OK'
            session['user'] = ret['data']
            flash('登录成功！')
            return redirect(url_for('index'))
        else:
            flash(ret['msg'])
            session['status'] = 'BAD'
    return render_template('login.html', form=form)


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))


@app.route("/reg", methods=['POST', 'GET'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        username = form.username.data
        userpass = form.userpass.data
        user = User(username=username, userpass=userpass)
        ret = user.reg_user(username, userpass)
        if ret['code'] == 0:
            # db.session.add(message)
            # db.session.commit()
            session['status'] = 'OK'
            flash('注册成功！')
            return redirect(url_for('login'))
        else:
            flash(ret['msg'])
            session['status'] = 'BAD'
    return render_template('reg.html', form=form)


@app.route('/code')
def get_code():
    image, str = validate_picture()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['verifycode'] = str
    return response
