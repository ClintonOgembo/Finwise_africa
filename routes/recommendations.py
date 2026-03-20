from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.transaction import Transaction
from models import db
from sqlalchemy import func
from datetime import datetime, date
from ml.advisor import generate_recommendations

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations')
@login_required
def index():
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

    expense_by_category = db.session.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= month_start
    ).group_by(Transaction.category).all()

    recommendations = generate_recommendations(total_income, total_expenses, expense_by_category)

    return render_template('recommendations/index.html',
        recommendations=recommendations,
        total_income=total_income,
        total_expenses=total_expenses
    )
