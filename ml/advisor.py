"""
advisor.py — Loads the trained ML model and generates personalised
financial recommendations based on a user's actual financial data.
"""

import os
import joblib
import numpy as np

_MODEL_DIR  = os.path.join(os.path.dirname(__file__), 'model_data')
_MODEL_PATH = os.path.join(_MODEL_DIR, 'advisor_model.pkl')
_META_PATH  = os.path.join(_MODEL_DIR, 'model_meta.pkl')


_model = None
_meta  = None

def _load_model():
    global _model, _meta
    if _model is None:
        if not os.path.exists(_MODEL_PATH):
            return False
        _model = joblib.load(_MODEL_PATH)
        _meta  = joblib.load(_META_PATH)
    return True


MESSAGES = {
    'rec_start_tracking': {
        'type': 'info', 'icon': '📊',
        'title': 'Start tracking your finances',
        'message': 'Add your income and expense transactions to receive personalised AI-powered financial advice tailored to your spending patterns.'
    },
    'rec_critical': {
        'type': 'danger', 'icon': '🚨',
        'title': 'Spending exceeds income',
        'message': 'Your expenses are higher than your income this month. This is unsustainable. Review all expense categories and identify areas to cut immediately to avoid debt.'
    },
    'rec_low_savings': {
        'type': 'danger', 'icon': '⚠️',
        'title': 'Very low savings rate',
        'message': 'You are saving less than 10% of your income. Financial experts recommend saving at least 20%. Start by cutting one non-essential expense category and redirecting that amount to savings.'
    },
    'rec_improve_savings': {
        'type': 'warning', 'icon': '📈',
        'title': 'Good start — push savings higher',
        'message': 'Your savings rate is between 10% and 20%. You are on the right track! Set a target to save 20% by gradually reducing discretionary spending such as entertainment or dining out.'
    },
    'rec_good_savings': {
        'type': 'success', 'icon': '✅',
        'title': 'Healthy savings rate',
        'message': 'You are saving between 20% and 30% of your income — well above average. Consider setting up a dedicated savings goal for a major purchase, education, or emergency fund.'
    },
    'rec_excellent': {
        'type': 'success', 'icon': '🌟',
        'title': 'Excellent financial discipline',
        'message': 'You are saving 30% or more of your income. Outstanding! Your surplus is large enough to begin building long-term wealth through investments.'
    },
    'rec_high_food': {
        'type': 'warning', 'icon': '🍽️',
        'title': 'High food spending detected',
        'message': 'Food and groceries are consuming more than 40% of your income. Try weekly meal planning, buying staples in bulk from wholesale markets, or reducing the frequency of eating out.'
    },
    'rec_high_transport': {
        'type': 'warning', 'icon': '🚌',
        'title': 'Transport costs are high',
        'message': 'Transport is taking more than 20% of your income. Consider using public transport (matatu, BRT), carpooling with colleagues, or planning errands in batches to reduce fuel costs.'
    },
    'rec_high_rent': {
        'type': 'warning', 'icon': '🏠',
        'title': 'Rent is a large portion of income',
        'message': 'Rent is consuming more than 40% of your income. Financial advisors recommend keeping housing costs below 30%. Consider splitting rent with a housemate or exploring lower-cost neighbourhoods.'
    },
    'rec_emergency_fund': {
        'type': 'info', 'icon': '🛡️',
        'title': 'Build your emergency fund',
        'message': 'Your current savings do not cover 3 months of expenses. Before investing, prioritise building an emergency fund of 3 to 6 months of living costs. Keep it in a liquid M-Pesa lock savings or money market account.'
    },
    'rec_invest': {
        'type': 'success', 'icon': '💹',
        'title': 'Ready to grow your wealth',
        'message': 'With a strong savings rate you are well positioned to invest. Consider NSE-listed Money Market Funds (e.g. CIC, Sanlam, Nabo), SACCOs for affordable credit, or Treasury Bills through the CBK mobile app.'
    },
}


def _extract_features(total_income, total_expenses, expense_by_category):
    """Convert raw financial data into the feature vector the model expects."""
    if total_income <= 0:
        return None

    cat = {c.lower(): amt for c, amt in expense_by_category}

    def ratio(keys):
        val = sum(cat.get(k.lower(), 0) for k in keys)
        return val / total_income

    savings_rate        = ((total_income - total_expenses) / total_income) * 100
    food_ratio          = ratio(['Food & Groceries'])
    transport_ratio     = ratio(['Transport & Fuel'])
    rent_ratio          = ratio(['Rent & Housing'])
    entertainment_ratio = ratio(['Entertainment'])
    utilities_ratio     = ratio(['Utilities (Water, Electricity)'])

    # Income level: 0=low, 1=medium, 2=high
    if total_income < 20000:
        income_level = 0
    elif total_income < 80000:
        income_level = 1
    else:
        income_level = 2

    return np.array([[
        savings_rate,
        food_ratio,
        transport_ratio,
        rent_ratio,
        entertainment_ratio,
        utilities_ratio,
        income_level,
    ]])


def generate_recommendations(total_income, total_expenses, expense_by_category):
    """
    Uses the trained ML model to predict which recommendations apply
    to this user, then returns the corresponding message cards.
    """
    # Case 1: No data yet
    if total_income == 0:
        return [MESSAGES['rec_start_tracking']]

    # Case 2: Model not trained yet — fall back to rule-based logic
    if not _load_model():
        return _rule_based_fallback(total_income, total_expenses, expense_by_category)

    # Case 3: Use ML model
    features = _extract_features(total_income, total_expenses, expense_by_category)
    if features is None:
        return [MESSAGES['rec_start_tracking']]

    rec_labels = _meta['rec_labels']
    predictions = _model.predict(features)[0]   
    probabilities = _model.predict_proba(features)  
    # Build recommendations from predicted labels
    recommendations = []
    for i, label in enumerate(rec_labels):
        if predictions[i] == 1 and label in MESSAGES:
            rec = MESSAGES[label].copy()
            # Add confidence score
            prob = probabilities[i][0][1] if hasattr(probabilities[i][0], '__len__') else probabilities[i][1]
            rec['confidence'] = round(prob * 100, 1)
            recommendations.append(rec)

    # If model predicts nothing (rare edge case), fall back
    if not recommendations:
        return _rule_based_fallback(total_income, total_expenses, expense_by_category)

    return recommendations



def _rule_based_fallback(total_income, total_expenses, expense_by_category):
    """Simple rule-based logic used before the model is trained."""
    recs = []
    if total_income == 0:
        return [MESSAGES['rec_start_tracking']]

    savings_rate = ((total_income - total_expenses) / total_income) * 100
    cat = {c.lower(): amt for c, amt in expense_by_category}
    food      = cat.get('food & groceries', 0)
    transport = cat.get('transport & fuel', 0)

    if savings_rate < 0:
        recs.append(MESSAGES['rec_critical'])
    elif savings_rate < 10:
        recs.append(MESSAGES['rec_low_savings'])
    elif savings_rate < 20:
        recs.append(MESSAGES['rec_improve_savings'])
    elif savings_rate < 30:
        recs.append(MESSAGES['rec_good_savings'])
    else:
        recs.append(MESSAGES['rec_excellent'])

    if total_income > 0:
        if food / total_income > 0.4:
            recs.append(MESSAGES['rec_high_food'])
        if transport / total_income > 0.2:
            recs.append(MESSAGES['rec_high_transport'])
        months = (total_income - total_expenses) / total_expenses if total_expenses > 0 else 999
        if months < 3:
            recs.append(MESSAGES['rec_emergency_fund'])
        if savings_rate >= 20:
            recs.append(MESSAGES['rec_invest'])

    return recs