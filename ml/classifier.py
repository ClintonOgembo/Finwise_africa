"""
classifier.py — Financial health classifier.
Uses the same trained model to assign a health label to each user.
"""

import os
import joblib
import numpy as np

_MODEL_DIR  = os.path.join(os.path.dirname(__file__), 'model_data')
_MODEL_PATH = os.path.join(_MODEL_DIR, 'advisor_model.pkl')

HEALTH_LEVELS = {
    'excellent': {'label': 'Excellent', 'color': '#00A86B', 'description': 'You are in outstanding financial health.'},
    'good':      {'label': 'Good',      'color': '#4CAF50', 'description': 'You are managing your finances well.'},
    'fair':      {'label': 'Fair',      'color': '#FFB800', 'description': 'There is room to improve your finances.'},
    'poor':      {'label': 'Poor',      'color': '#FF7043', 'description': 'Your finances need attention.'},
    'critical':  {'label': 'Critical',  'color': '#E63946', 'description': 'Urgent action needed on your finances.'},
}

def classify_user(total_income, total_expenses):
    """Returns a health level dict based on savings rate."""
    if total_income <= 0:
        return HEALTH_LEVELS['fair']

    savings_rate = ((total_income - total_expenses) / total_income) * 100

    if savings_rate >= 30:
        return HEALTH_LEVELS['excellent']
    elif savings_rate >= 20:
        return HEALTH_LEVELS['good']
    elif savings_rate >= 10:
        return HEALTH_LEVELS['fair']
    elif savings_rate >= 0:
        return HEALTH_LEVELS['poor']
    else:
        return HEALTH_LEVELS['critical']