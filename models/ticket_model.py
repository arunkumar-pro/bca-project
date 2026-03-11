from bson import ObjectId
from database.mongodb_connection import get_db
from datetime import datetime

STATUS_OPEN = 'Open'
STATUS_IN_PROGRESS = 'In Progress'
STATUS_CLOSED = 'Closed'

PRIORITY_LOW = 'Low'
PRIORITY_MEDIUM = 'Medium'
PRIORITY_HIGH = 'High'
PRIORITY_CRITICAL = 'Critical'

class Ticket:
    @staticmethod
    def create(title, description, category, priority, user_id, user_email, username):
        db = get_db()
        # Auto-increment ticket ID
        counter = db.counters.find_one_and_update(
            {'_id': 'ticket_id'},
            {'$inc': {'seq': 1}},
            upsert=True,
            return_document=True
        )
        ticket_number = f"TKT-{counter['seq']:04d}"
        
        ticket_data = {
            'ticket_number': ticket_number,
            'title': title,
            'description': description,
            'category': category,
            'priority': priority,
            'status': STATUS_OPEN,
            'user_id': user_id,
            'user_email': user_email,
            'username': username,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'comments': [],
            'assigned_to': None
        }
        result = db.tickets.insert_one(ticket_data)
        ticket_data['_id'] = result.inserted_id
        return ticket_data

    @staticmethod
    def get_by_id(ticket_id):
        db = get_db()
        try:
            return db.tickets.find_one({'_id': ObjectId(ticket_id)})
        except:
            return None

    @staticmethod
    def get_by_user(user_id, page=1, per_page=10, search='', status_filter=''):
        db = get_db()
        query = {'user_id': user_id}
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'ticket_number': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        if status_filter:
            query['status'] = status_filter
        
        total = db.tickets.count_documents(query)
        tickets = list(db.tickets.find(query)
                      .sort('created_at', -1)
                      .skip((page - 1) * per_page)
                      .limit(per_page))
        return tickets, total

    @staticmethod
    def get_all(page=1, per_page=10, search='', status_filter='', priority_filter=''):
        db = get_db()
        query = {}
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'ticket_number': {'$regex': search, '$options': 'i'}},
                {'username': {'$regex': search, '$options': 'i'}}
            ]
        if status_filter:
            query['status'] = status_filter
        if priority_filter:
            query['priority'] = priority_filter

        total = db.tickets.count_documents(query)
        tickets = list(db.tickets.find(query)
                      .sort('created_at', -1)
                      .skip((page - 1) * per_page)
                      .limit(per_page))
        return tickets, total

    @staticmethod
    def update_status(ticket_id, status, admin_comment='', admin_name=''):
        db = get_db()
        update = {
            '$set': {
                'status': status,
                'updated_at': datetime.utcnow()
            }
        }
        if admin_comment:
            update['$push'] = {
                'comments': {
                    'text': admin_comment,
                    'author': admin_name,
                    'timestamp': datetime.utcnow(),
                    'type': 'admin'
                }
            }
        db.tickets.update_one({'_id': ObjectId(ticket_id)}, update)

    @staticmethod
    def add_comment(ticket_id, comment, author, comment_type='user'):
        db = get_db()
        db.tickets.update_one(
            {'_id': ObjectId(ticket_id)},
            {
                '$push': {
                    'comments': {
                        'text': comment,
                        'author': author,
                        'timestamp': datetime.utcnow(),
                        'type': comment_type
                    }
                },
                '$set': {'updated_at': datetime.utcnow()}
            }
        )

    @staticmethod
    def get_stats():
        db = get_db()
        stats = {
            'total': db.tickets.count_documents({}),
            'open': db.tickets.count_documents({'status': STATUS_OPEN}),
            'in_progress': db.tickets.count_documents({'status': STATUS_IN_PROGRESS}),
            'closed': db.tickets.count_documents({'status': STATUS_CLOSED}),
            'critical': db.tickets.count_documents({'priority': PRIORITY_CRITICAL}),
            'high': db.tickets.count_documents({'priority': PRIORITY_HIGH}),
        }
        return stats

    @staticmethod
    def delete(ticket_id):
        db = get_db()
        db.tickets.delete_one({'_id': ObjectId(ticket_id)})
