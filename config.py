import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/support_ticket_db_bca')
    
    # Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'arunkumarr@dckap.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'vhrc ydnu vtny zsci')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@support.com')
    
    # Pagination
    TICKETS_PER_PAGE = 10
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
