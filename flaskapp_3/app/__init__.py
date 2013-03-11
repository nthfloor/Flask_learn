import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#setup Flask
app = Flask(__name__)
app.config.from_object('config')

#setup database TODO
db = SQLAlchemy(app)
lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

#setup openid
#oid = OpenID(app, os.path.join(basedir,'tmp'))
oid = OpenID(app)

from app import views,models
