from flask_login import UserMixin
from bson import ObjectId
from database.mongodb_connection import get_db
import bcrypt
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.role = user_data.get('role', 'user')
        self.created_at = user_data.get('created_at', datetime.utcnow())
        self.is_active_account = user_data.get('is_active', True)

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.role == 'admin'

    @staticmethod
    def create(username, email, password, role='user'):
        db = get_db()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_pw,
            'role': role,
            'created_at': datetime.utcnow(),
            'is_active': True
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return User(user_data)

    @staticmethod
    def get_by_email(email):
        db = get_db()
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        try:
            user_data = db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User(user_data)
        except:
            pass
        return None

    @staticmethod
    def email_exists(email):
        db = get_db()
        return db.users.find_one({'email': email}) is not None

    @staticmethod
    def verify_password(email, password):
        db = get_db()
        user_data = db.users.find_one({'email': email})
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            return User(user_data)
        return None

    @staticmethod
    def get_all_users():
        db = get_db()
        return list(db.users.find({'role': 'user'}))
