from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField                            #imports
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


#registartion form
class RegisterForm(FlaskForm):
    #method to validate the username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken")
    #method to validate the email address
    def validate_email_address(self, email_address):
        email = User.query.filter_by(email=email_address.data).first()
        if email:
            raise ValidationError("Email address already taken")
        
    username = StringField(label="Username", validators=[Length(min=2, max=10), DataRequired()])
    email_address = StringField(label="Email Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6, max=10), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Register")
#login form
class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password=PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")
#add items form
class AddItems(FlaskForm):
    name=StringField(label="Name", validators=[DataRequired()])
    barcode=StringField(label="Barcode", validators=[Length(min=10, max=10),DataRequired()])
    description=StringField(label="Description", validators=[Length(min=30, max=1024),DataRequired()])
    price=  StringField(label="Price", validators=[DataRequired()])
    img_url=StringField(label="Image URL", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
 #purchase form   
class PurchaseForm(FlaskForm):
      submit = SubmitField(label="Purchase")
  #sell form    
class SellForm(FlaskForm):
      submit = SubmitField(label="Sell item")