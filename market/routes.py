from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm




@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    books = Item.query.all()
    return render_template('market.html', books=books)

@app.route("/register", methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():

        created_user = User(username=form.username.data, 
                             email=form.email_address.data,
                             password_hash=form.password1.data)
        db.session.add(created_user)
        db.session.commit()
        
        flash('Account created successfully!', 'success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'there was an error:{err_msg}', category='danger')
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
