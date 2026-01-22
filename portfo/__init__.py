from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfo.sqlite'  # Change to match your app
app.secret_key = b'dfjiekdkdieidkdk'  # Replace with secure secret key in production

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect here if user is not logged in
login_manager.login_message_category = 'info'

# Define user loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from portfo.models import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

# Import routes and models after app and extensions are set up
from portfo import routes
