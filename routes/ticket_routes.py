from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from models.ticket_model import Ticket
from bson import ObjectId
import math

ticket_bp = Blueprint('tickets', __name__)

CATEGORIES = ['Technical Support', 'Billing', 'Account Issue', 'Feature Request', 'Bug Report', 'General Inquiry']
PRIORITIES = ['Low', 'Medium', 'High', 'Critical']
STATUSES = ['Open', 'In Progress', 'Closed']

@ticket_bp.route('/')
@login_required
def my_tickets():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    per_page = current_app.config.get('TICKETS_PER_PAGE', 10)
    
    tickets, total = Ticket.get_by_user(
        current_user.id, page, per_page, search, status_filter
    )
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return render_template('dashboard.html',
        tickets=tickets,
        page=page,
        total_pages=total_pages,
        total=total,
        search=search,
        status_filter=status_filter,
        statuses=STATUSES
    )

@ticket_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '')
        priority = request.form.get('priority', 'Medium')
        
        if not title or not description or not category:
            flash('All fields are required.', 'danger')
        else:
            ticket = Ticket.create(
                title, description, category, priority,
                current_user.id, current_user.email, current_user.username
            )
            flash(f'Ticket {ticket["ticket_number"]} created successfully!', 'success')
            return redirect(url_for('tickets.my_tickets'))
    
    return render_template('create_ticket.html', categories=CATEGORIES, priorities=PRIORITIES)

@ticket_bp.route('/<ticket_id>')
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.get_by_id(ticket_id)
    if not ticket:
        flash('Ticket not found.', 'danger')
        return redirect(url_for('tickets.my_tickets'))
    
    if str(ticket['user_id']) != current_user.id and not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('tickets.my_tickets'))
    
    return render_template('view_ticket.html', ticket=ticket)

@ticket_bp.route('/<ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.get_by_id(ticket_id)
    if not ticket:
        flash('Ticket not found.', 'danger')
        return redirect(url_for('tickets.my_tickets'))
    
    comment = request.form.get('comment', '').strip()
    if comment:
        Ticket.add_comment(ticket_id, comment, current_user.username)
        flash('Comment added.', 'success')
    
    return redirect(url_for('tickets.view_ticket', ticket_id=ticket_id))

# ─── API Endpoints ────────────────────────────────────────────────
@ticket_bp.route('/api/tickets', methods=['GET'])
@login_required
def api_get_tickets():
    tickets, total = Ticket.get_by_user(current_user.id)
    result = []
    for t in tickets:
        t['_id'] = str(t['_id'])
        t['created_at'] = t['created_at'].isoformat()
        t['updated_at'] = t['updated_at'].isoformat()
        result.append(t)
    return jsonify({'tickets': result, 'total': total})

@ticket_bp.route('/api/tickets/<ticket_id>', methods=['GET'])
@login_required
def api_get_ticket(ticket_id):
    ticket = Ticket.get_by_id(ticket_id)
    if not ticket:
        return jsonify({'error': 'Not found'}), 404
    ticket['_id'] = str(ticket['_id'])
    ticket['created_at'] = ticket['created_at'].isoformat()
    return jsonify(ticket)

@ticket_bp.route('/api/tickets', methods=['POST'])
@login_required
def api_create_ticket():
    data = request.get_json()
    ticket = Ticket.create(
        data['title'], data['description'], data['category'],
        data.get('priority', 'Medium'),
        current_user.id, current_user.email, current_user.username
    )
    ticket['_id'] = str(ticket['_id'])
    return jsonify(ticket), 201
