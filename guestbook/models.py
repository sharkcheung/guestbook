# -*- coding: utf-8 -*-
"""
    :author: SharkCheung
    :copyright: © 2020 Shark Cheung <563049899@qq.com>
    :license: MIT, see LICENSE for more details.
"""
import json
from datetime import datetime

from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from guestbook import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    userpass = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def check_login(self, user_name, user_pass):
        ret = self.query.filter_by(username=user_name).first()
        if ret:
            # 生成密码
            pwd = ret.userpass
            # 对比密码
            result = check_password_hash(pwd, user_pass)

            if result:
                retjson = {'code': 0, 'msg': '登录成功！', 'data': ret.to_dict()}
            else:
                retjson = {'code': -1, 'msg': '密码不正确！', 'data': []}
        else:
            retjson = {'code': -1, 'msg': '账号不存在！', 'data': []}
        return retjson

    def to_dict(self):
        # 数据查询对象转字典
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def reg_user(self, user_name, user_pass):
        ret = self.query.filter_by(username=user_name).first()
        if ret:
            retjson = {'code': -1, 'msg': '账号已被注册！', 'data': []}
        else:
            # 生成密码
            pwd = generate_password_hash(user_pass)
            user = User(username=user_name, userpass=pwd)
            db.session.add(user)
            db.session.commit()
            # print(user)
            if user:
                retjson = {'code': 0, 'msg': '登录成功！', 'data': ret}
            else:
                retjson = {'code': -1, 'msg': '密码不正确！', 'data': []}
        return retjson


if __name__ == '__main__':
    db.create_all()
