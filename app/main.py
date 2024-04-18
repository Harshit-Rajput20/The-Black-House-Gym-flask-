from flask import Flask, render_template
from views.regester import signup_bp
from views.signup import signup_blueprint
from models.database import db
from models.sessions import Session
from models.package import PackageSignupTable
from models.user import User
from views.packageview import package_bp
from sqlalchemy import inspect
from envsecrets.config import Config
from views.login import login_blueprint
app = Flask(__name__)
app.config.from_object(Config)

# Specify the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db:3306/memberInfo'

# Initialize the database
db.init_app(app)

# Register the blueprint for signup functionality
# app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(signup_blueprint)
app.register_blueprint(package_bp)
app.register_blueprint(login_blueprint)

def tables_exist():
    with app.app_context():
        inspector = inspect(db.engine)
        return all(table in inspector.get_table_names() for table in ['sessions','user','package_signuptable'])




# Function to check if there is any data in the tables
def data_exists():
    with app.app_context():
        return any(db.session.query(model).count() > 0 for model in [PackageSignupTable,Session,User])
    

if not tables_exist():
    with app.app_context():
        db.create_all()



# Define routes and views
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)
