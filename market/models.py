from market import db, login_manager
from market import bcrypt
from sqlalchemy import Numeric
from decimal import Decimal
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    budget = db.Column(Numeric(precision=10, scale=2), nullable=False, default=1000)
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

    def can_purchase(self,item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=False)
    img_url=db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def __repr__(self):
        return f'Item {self.name}'
    def buy(self, user):
         self.owner_id=user.id
         user.budget-=self.price
         db.session.commit()
    
    def sell(self, user):
         self.owner_id=None
         user.budget+=self.price
         db.session.commit()
         
