from market import app, db
from flask import render_template, redirect, url_for, flash,request
from market.models import Item, User                                   ## import extensions from the market package
from market.forms import RegisterForm, AddItems
from market.forms import LoginForm,PurchaseForm,SellForm
from flask_login import login_user, logout_user,login_required,current_user #for the login functionalities



@app.route('/')
def home_page():
    return render_template('home.html')

@app.route("/market", methods=["POST", "GET"])
@login_required
def market_page():
    selling_form=SellForm() #create a form for the sell functionality
    purchase_form=PurchaseForm() #created a form in forms for purchase func
    if request.method =="POST":
        #purchase item
        purchased_item=request.form.get('purchased_item')
        print(purchased_item)
        item_obj=Item.query.get(purchased_item)
        print(item_obj)
        if not item_obj:
            flash("USER NOT FOUND!!", category='danger')
        elif item_obj:
            #created a method can_purchase in User class
            if current_user.can_purchase(item_obj):
                #create a buy method in Item for the buy func
                item_obj.buy(current_user)
                flash(f'{purchased_item} has been purchased by {current_user.username}',category="success")
                
            else:
                flash(f'You do not have enough funds', category="danger")
        #sell item
        sold_item=request.form.get('sold_item')
        s_item_obj=Item.query.get(sold_item)
        if s_item_obj:
            if current_user.can_sell(s_item_obj): #create a method can_sell in user to help with the functionality
                s_item_obj.sell(current_user) #create a method sell in item to help with the functionality
                flash(f'{purchased_item} has been sold by {current_user.username}',category="success")
            else:
                flash("Something went wrong", category="danger")    
        return redirect(url_for('market_page'))            
   
    if request.method =='GET':
        
        books = Item.query.filter_by(owner_id=None)
        owned_books=Item.query.filter_by(owner_id=current_user.id)
        return render_template('market.html', books=books, purchase_form=purchase_form, owned_books=owned_books, sell_form=selling_form)
#register page
@app.route("/register", methods=['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():

        created_user = User(username=form.username.data, 
                             email=form.email_address.data, #details to be registered
                             password=form.password1.data)
        db.session.add(created_user) #add to the database
        db.session.commit() #commit
        login_user(created_user) #the created user get login to the ap after the account is created
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
    if form.validate_on_submit(): #the form is validated before it is submitted
        attempted_user=User.query.filter_by(username=form.username.data).first() #filter the user by the username input
        if attempted_user and attempted_user.check_password(
            attempted_password=form.password.data):
            login_user(attempted_user) #this allows the user to be loggged in once the password and email are confirmed
            flash(f'You are now logged in:{attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Invalid username or password',category= 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')

def logout_page():
    logout_user() #logs out the user
    flash('logged out successfull!', category='info')
    return redirect(url_for('home_page'))
href="{{ url_for('logout_page') }}"
#add items form
@app.route('/addItems', methods=['POST', 'GET'])
def add_items():
    form = AddItems()
    if form.validate_on_submit() and request.method == 'POST':
        new_item = Item(name=form.name.data, description=form.description.data, price=form.price.data, barcode=form.barcode.data, img_url=form.img_url.data)
        # new_item.owner_id = current_user.id
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', category='success')
        return redirect(url_for('market_page'))
    
    return render_template('addItems.html', form=form)

    

if __name__ == "__main__":
    app.run(debug=True) 
