
#creates a package called market

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db' # attach the app to sqlalchemy
app.config['SECRET_KEY']='d5f34bcec7282739912117f6' #generate a secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
from market import routes
