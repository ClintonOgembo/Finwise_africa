"""
Savings Predictor (ML module - to be expanded with scikit-learn models)
Predicts future savings based on current trends.
"""

def predict_savings(monthly_savings, months=6):
    """Simple linear prediction — replace with trained ML model later."""
    return [monthly_savings * (i + 1) for i in range(months)]
