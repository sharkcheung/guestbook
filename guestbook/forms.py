# -*- coding: utf-8 -*-
"""
    :author: SharkCheung
    :copyright: © 2020 Shark Cheung <563049899@qq.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import session
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class HelloForm(FlaskForm):
    name = StringField('姓名：', description="* 长度必须在1-20之间", validators=[DataRequired(), Length(1, 20, '姓名长度必须在1-20之间')], render_kw={"placeholder": "姓名", "required": "required", "class": "form-control"})
    body = TextAreaField('留言内容：', description="* 长度必须在1-200之间", validators=[DataRequired(), Length(1, 200, '留言内容长度必须在1-200之间')], render_kw={"placeholder": "留言内容", "required": "required", "class": "form-control"})
    verifycode = StringField('验证码：', description="* 区分大小写", validators=[DataRequired(), Length(1, 4, '验证码为4位字符串')], render_kw={"placeholder": "验证码", "required": "required", "class": "form-control"})
    # recaptcha = RecaptchaField()
    submit = SubmitField('提交', render_kw={"class": "btn btn-secondary"})

    def validate(self):
        check_validate = super(HelloForm, self).validate()

        # If validator no pass
        if not check_validate:
            return False

        # Check the user whether exist.
        verifycode = self.verifycode.data
        print(verifycode, session['verifycode'])
        if verifycode != session['verifycode']:
            self.verifycode.errors.append('验证码不正确！')
            return False
        return True
