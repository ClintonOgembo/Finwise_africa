"""
User Financial Classifier (ML module - to be expanded)
Classifies users into financial health categories using spending ratios.
"""

def classify_user(total_income, total_expenses, savings_goals_count):
    if total_income == 0:
        return 'unclassified'
    
    savings_rate = (total_income - total_expenses) / total_income

    if savings_rate >= 0.3:
        return 'excellent'
    elif savings_rate >= 0.2:
        return 'good'
    elif savings_rate >= 0.1:
        return 'fair'
    elif savings_rate >= 0:
        return 'poor'
    else:
        return 'critical'
