from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
from models.ticket_model import Ticket
from models.user_model import User
import math

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = Ticket.get_stats()
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    per_page = current_app.config.get('TICKETS_PER_PAGE', 10)
    
    tickets, total = Ticket.get_all(page, per_page, search, status_filter, priority_filter)
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    
    return render_template('admin/dashboard.html',
        stats=stats,
        tickets=tickets,
        page=page,
        total_pages=total_pages,
        total=total,
        search=search,
        status_filter=status_filter,
        priority_filter=priority_filter
    )

@admin_bp.route('/ticket/<ticket_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_ticket(ticket_id):
    ticket = Ticket.get_by_id(ticket_id)
    if not ticket:
        flash('Ticket not found.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        new_status = request.form.get('status')
        comment = request.form.get('comment', '').strip()
        Ticket.update_status(ticket_id, new_status, comment, current_user.username)
        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('admin.manage_ticket', ticket_id=ticket_id))
    
    return render_template('admin/manage_ticket.html', ticket=ticket,
                           statuses=['Open', 'In Progress', 'Closed'])

@admin_bp.route('/ticket/<ticket_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_ticket(ticket_id):
    Ticket.delete(ticket_id)
    flash('Ticket deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.get_all_users()
    return render_template('admin/users.html', users=all_users)

# ─── Admin API ────────────────────────────────────────────────────
@admin_bp.route('/api/stats')
@login_required
@admin_required
def api_stats():
    return jsonify(Ticket.get_stats())

@admin_bp.route('/api/tickets/<ticket_id>/status', methods=['PUT'])
@login_required
@admin_required
def api_update_status(ticket_id):
    data = request.get_json()
    Ticket.update_status(ticket_id, data['status'], data.get('comment', ''), current_user.username)
    return jsonify({'success': True})
