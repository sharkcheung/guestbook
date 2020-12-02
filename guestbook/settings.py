# -*- coding: utf-8 -*-
"""
    :author: SharkCheung
    :copyright: © 2020 Shark Cheung <563049899@qq.com>
    :license: MIT, see LICENSE for more details.
"""
import os
import sys

from guestbook import app

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
