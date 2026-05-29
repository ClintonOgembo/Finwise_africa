from . import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.type} {self.amount}>'


EXPENSE_CATEGORIES = [
    'Food & Groceries',
    'Transport & Fuel',
    'Rent & Housing',
    'Utilities (Water, Electricity)',
    'Mobile & Internet',
    'Healthcare',
    'Education',
    'Clothing',
    'Entertainment',
    'Business Expenses',
    'Family Support',
    'Church / Tithe',
    'Savings Contribution',
    'Other',
]

INCOME_CATEGORIES = [
    'Salary / Employment',
    'Business / Self-Employment',
    'Freelance / Side Hustle',
    'M-Pesa / Mobile Money',
    'Agricultural Income',
    'Rental Income',
    'Investments',
    'Family Support Received',
    'Other',
]
