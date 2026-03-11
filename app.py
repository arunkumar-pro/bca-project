from flask import Flask
from flask_login import LoginManager
from config import Config
from database.mongodb_connection import init_db
from routes.auth_routes import auth_bp
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp
from models.user_model import User

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

init_db(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(ticket_bp, url_prefix='/tickets')
app.register_blueprint(admin_bp, url_prefix='/admin')

from routes.main_routes import main_bp
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
