from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.transaction import Transaction, EXPENSE_CATEGORIES, INCOME_CATEGORIES
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions')
@login_required
def index():
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).all()
    return render_template('transactions/index.html', transactions=transactions)

@transactions_bp.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        t = Transaction(
            user_id=current_user.id,
            type=request.form.get('type'),
            category=request.form.get('category'),
            amount=float(request.form.get('amount')),
            description=request.form.get('description'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        )
        db.session.add(t)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('transactions.index'))
    return render_template('transactions/add.html',
        expense_categories=EXPENSE_CATEGORIES,
        income_categories=INCOME_CATEGORIES
    )

@transactions_bp.route('/transactions/delete/<int:id>')
@login_required
def delete(id):
    t = Transaction.query.get_or_404(id)
    if t.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('transactions.index'))
    db.session.delete(t)
    db.session.commit()
    flash('Transaction deleted.', 'success')
    return redirect(url_for('transactions.index'))
