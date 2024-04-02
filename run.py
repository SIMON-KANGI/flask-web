from market import app #import app/db from the market package
from market import db

if __name__ == '__main__':
    with app.app_context():
        
     db.create_all() #creating database
     app.run(debug=True) #refreshing the project when changes are made