"""
AI Advisory Module
Generates personalized financial recommendations based on user data.
Uses rule-based logic + ML classification (expandable).
"""

def generate_recommendations(total_income, total_expenses, expense_by_category):
    recommendations = []
    
    if total_income == 0:
        recommendations.append({
            'type': 'info',
            'icon': '📊',
            'title': 'Start Tracking',
            'message': 'Add your income and expenses to receive personalized recommendations.'
        })
        return recommendations

    savings_rate = ((total_income - total_expenses) / total_income) * 100 if total_income > 0 else 0
    expense_dict = {cat: amt for cat, amt in expense_by_category}

    # Savings rate advice
    if savings_rate < 10:
        recommendations.append({
            'type': 'danger',
            'icon': '⚠️',
            'title': 'Low Savings Rate',
            'message': f'You are saving only {savings_rate:.1f}% of your income. Aim for at least 20%. Try cutting discretionary spending.'
        })
    elif savings_rate < 20:
        recommendations.append({
            'type': 'warning',
            'icon': '💡',
            'title': 'Improve Your Savings',
            'message': f'Your savings rate is {savings_rate:.1f}%. Good progress! Try to reach 20% by reducing non-essential expenses.'
        })
    else:
        recommendations.append({
            'type': 'success',
            'icon': '🌟',
            'title': 'Excellent Savings Rate',
            'message': f'You are saving {savings_rate:.1f}% of your income. Great work! Consider investing the surplus for long-term wealth building.'
        })

    # Food spending
    food = expense_dict.get('Food & Groceries', 0)
    if total_income > 0 and (food / total_income) > 0.4:
        recommendations.append({
            'type': 'warning',
            'icon': '🍽️',
            'title': 'High Food Spending',
            'message': f'Food & Groceries take up {(food/total_income*100):.1f}% of your income. Try meal planning or buying in bulk to reduce costs.'
        })

    # Transport spending
    transport = expense_dict.get('Transport & Fuel', 0)
    if total_income > 0 and (transport / total_income) > 0.2:
        recommendations.append({
            'type': 'warning',
            'icon': '🚗',
            'title': 'High Transport Costs',
            'message': f'Transport takes {(transport/total_income*100):.1f}% of your income. Consider carpooling or public transport to save more.'
        })

    # Emergency fund advice
    if savings_rate > 0:
        months_covered = (total_income - total_expenses) / total_expenses if total_expenses > 0 else 0
        if months_covered < 3:
            recommendations.append({
                'type': 'info',
                'icon': '🛡️',
                'title': 'Build an Emergency Fund',
                'message': 'Aim to save 3-6 months of expenses as an emergency fund before other investments.'
            })

    # Investment advice
    if savings_rate >= 20:
        recommendations.append({
            'type': 'success',
            'icon': '📈',
            'title': 'Start Investing',
            'message': 'With a healthy savings rate, consider NSE (Nairobi Stock Exchange), Money Market Funds, or SACCOs to grow your wealth.'
        })

    return recommendations
