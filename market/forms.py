from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken")
        
    def validate_email_address(self, email_address):
        email = User.query.filter_by(email=email_address.data).first()
        if email:
            raise ValidationError("Email address already taken")
        
    username = StringField(label="Username", validators=[Length(min=2, max=10), DataRequired()])
    email_address = StringField(label="Email Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6, max=10), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password=PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")