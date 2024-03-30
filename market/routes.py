from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm
from market.forms import LoginForm
from flask_login import login_user, logout_user,login_required



@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/market")
@login_required
def market_page():
    books = Item.query.all()
    return render_template('market.html', books=books)

@app.route("/register", methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():

        created_user = User(username=form.username.data, 
                             email=form.email_address.data,
                             password=form.password1.data)
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        flash(f'Account created successfully!.You are now logged in as {created_user.username}',category="success")
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}', category='danger')
    return render_template('register.html', form=form)
@app.route('/login',methods=['POST', 'GET'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You are now logged in:{attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Invalid username or password',category= 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')

def logout_page():
    logout_user()
    flash('logged out successfull!', category='info')
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run(debug=True) 
