from market import db, login_manager
from market import bcrypt

from flask_login import UserMixin, login_user, login_required, logout_user, current_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    budget=db.Column(db.Integer() ,nullable=False,default=1000)
    items = db.relationship('Item', backref='owner', lazy=True)
    
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_password_text):
        self.password_hash = bcrypt.generate_password_hash(plain_password_text).decode('utf-8')
    
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
            
    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
