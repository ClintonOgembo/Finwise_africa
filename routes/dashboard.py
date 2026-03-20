from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.transaction import Transaction
from models.savings import Savings
from sqlalchemy import func
from models import db
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Current month summary
    now = datetime.utcnow()
    month_start = date(now.year, now.month, 1)

    total_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        Transaction.date >= month_start
    ).scalar() or 0

    total_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= month_start
    ).scalar() or 0

    balance = total_income - total_expenses
    savings_goals = Savings.query.filter_by(user_id=current_user.id).all()

    # Recent transactions
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc()).limit(5).all()

    # Expense breakdown by category (for chart)
    expense_by_category = db.session.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= month_start
    ).group_by(Transaction.category).all()

    return render_template('dashboard/index.html',
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        savings_goals=savings_goals,
        recent_transactions=recent_transactions,
        expense_by_category=expense_by_category
    )
