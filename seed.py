"""
Seed script to create admin user and sample tickets for demo.
Run: python seed.py
"""
from app import app
from database.mongodb_connection import get_db
from models.user_model import User
from models.ticket_model import Ticket
import bcrypt
from datetime import datetime

def seed():
    with app.app_context():
        db = get_db()
        
        # Clear existing data
        db.users.delete_many({})
        db.tickets.delete_many({})
        db.counters.delete_many({})
        print("Cleared existing data.")

        # Create admin
        admin_pw = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt())
        db.users.insert_one({
            'username': 'Admin',
            'email': 'admin@demo.com',
            'password': admin_pw,
            'role': 'admin',
            'created_at': datetime.utcnow(),
            'is_active': True
        })
        print("✅ Admin created: admin@demo.com / admin123")

        # Create sample users
        users = [
            ('Arjun Kumar', 'arjun@test.com'),
            ('Priya Sharma', 'priya@test.com'),
            ('Rahul Verma', 'rahul@test.com'),
        ]
        user_ids = []
        for name, email in users:
            pw = bcrypt.hashpw('user123'.encode(), bcrypt.gensalt())
            result = db.users.insert_one({
                'username': name, 'email': email, 'password': pw,
                'role': 'user', 'created_at': datetime.utcnow(), 'is_active': True
            })
            user_ids.append((str(result.inserted_id), email, name))
        print(f"✅ {len(users)} sample users created (password: user123)")

        # Create sample tickets
        sample_tickets = [
            ('Cannot login to my account', 'I am unable to log in. It says invalid credentials but I reset my password.', 'Account Issue', 'High', 0),
            ('Payment not processed', 'My payment was deducted but order not placed. Transaction ID: TXN123456', 'Billing', 'Critical', 1),
            ('Feature request: Dark mode', 'Please add dark mode support to the dashboard.', 'Feature Request', 'Low', 2),
            ('Bug in ticket search', 'Search results are not filtering correctly by date range.', 'Bug Report', 'Medium', 0),
            ('Email notifications delayed', 'I am receiving email notifications 2+ hours late.', 'Technical Support', 'Medium', 1),
        ]
        for title, desc, cat, pri, uid_idx in sample_tickets:
            uid, email, uname = user_ids[uid_idx]
            Ticket.create(title, desc, cat, pri, uid, email, uname)
        print(f"✅ {len(sample_tickets)} sample tickets created")
        print("\n🚀 Seed complete! Run: python app.py")

if __name__ == '__main__':
    seed()
