"""
train.py — Run this ONCE to train and save the ML model.
Usage: python ml/train.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os


FEATURE_NAMES = [
    'savings_rate',       
    'food_ratio',         
    'transport_ratio',    
    'rent_ratio',         
    'entertainment_ratio',
    'utilities_ratio',    
    'income_level',       
]

# ── Recommendation labels ──────────────────────────────────────────────────────
REC_LABELS = [
    'rec_critical',       
    'rec_low_savings',    
    'rec_improve_savings',
    'rec_good_savings',   
    'rec_excellent',      
    'rec_high_food',      
    'rec_high_transport', 
    'rec_high_rent',      
    'rec_emergency_fund', 
    'rec_invest',         
    'rec_start_tracking', 
]

def generate_synthetic_data(n_samples=3000):
    """
    Generate realistic synthetic financial data representing
    Kenyan and African user profiles.
    """
    np.random.seed(42)
    data = []

    for _ in range(n_samples):
        # Simulate income levels (KES/month)
        income_bracket = np.random.choice([0, 1, 2], p=[0.45, 0.40, 0.15])
        if income_bracket == 0:
            income = np.random.uniform(5000, 20000)
        elif income_bracket == 1:
            income = np.random.uniform(20000, 80000)
        else:
            income = np.random.uniform(80000, 300000)

        # Simulate spending ratios based on income bracket
        
        if income_bracket == 0:
            food_ratio      = np.clip(np.random.beta(3, 3) * 0.7, 0.1, 0.75)
            transport_ratio = np.clip(np.random.beta(2, 4) * 0.4, 0.05, 0.45)
            rent_ratio      = np.clip(np.random.beta(2, 3) * 0.5, 0.1, 0.6)
        elif income_bracket == 1:
            food_ratio      = np.clip(np.random.beta(2, 4) * 0.5, 0.1, 0.55)
            transport_ratio = np.clip(np.random.beta(2, 4) * 0.3, 0.05, 0.35)
            rent_ratio      = np.clip(np.random.beta(2, 3) * 0.4, 0.1, 0.5)
        else:
            food_ratio      = np.clip(np.random.beta(2, 6) * 0.3, 0.05, 0.35)
            transport_ratio = np.clip(np.random.beta(2, 5) * 0.2, 0.03, 0.25)
            rent_ratio      = np.clip(np.random.beta(2, 4) * 0.3, 0.05, 0.4)

        entertainment_ratio = np.clip(np.random.beta(1.5, 6) * 0.2, 0, 0.25)
        utilities_ratio     = np.clip(np.random.beta(2, 6) * 0.15, 0.02, 0.2)

        total_expense_ratio = food_ratio + transport_ratio + rent_ratio + entertainment_ratio + utilities_ratio
        total_expense_ratio = min(total_expense_ratio, 1.2)  # allow slight overspend

        savings_rate = (1 - total_expense_ratio) * 100

        # Build recommendation labels 
        labels = {r: 0 for r in REC_LABELS}
        labels['rec_start_tracking'] = 0  

        expenses = income * total_expense_ratio
        months_covered = (income - expenses) / expenses if expenses > 0 else 999

        if savings_rate < 0:
            labels['rec_critical'] = 1
        elif savings_rate < 10:
            labels['rec_low_savings'] = 1
        elif savings_rate < 20:
            labels['rec_improve_savings'] = 1
        elif savings_rate < 30:
            labels['rec_good_savings'] = 1
        else:
            labels['rec_excellent'] = 1

        if food_ratio > 0.4:
            labels['rec_high_food'] = 1
        if transport_ratio > 0.2:
            labels['rec_high_transport'] = 1
        if rent_ratio > 0.4:
            labels['rec_high_rent'] = 1
        if months_covered < 3 and savings_rate >= 0:
            labels['rec_emergency_fund'] = 1
        if savings_rate >= 20:
            labels['rec_invest'] = 1

        row = [
            savings_rate,
            food_ratio,
            transport_ratio,
            rent_ratio,
            entertainment_ratio,
            utilities_ratio,
            income_bracket,
        ] + [labels[r] for r in REC_LABELS]

        data.append(row)

    columns = FEATURE_NAMES + REC_LABELS
    return pd.DataFrame(data, columns=columns)


def train_and_save():
    print("Generating synthetic training data...")
    df = generate_synthetic_data(3000)
    print(f"  Dataset size: {len(df)} samples")

    X = df[FEATURE_NAMES].values
    y = df[REC_LABELS].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest model...")
    base_clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        class_weight='balanced'
    )
    model = MultiOutputClassifier(base_clf, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("\nModel evaluation (sample labels):")
    for i, label in enumerate(REC_LABELS[:5]):
        tp = ((y_test[:, i] == 1) & (y_pred[:, i] == 1)).sum()
        fp = ((y_test[:, i] == 0) & (y_pred[:, i] == 1)).sum()
        fn = ((y_test[:, i] == 1) & (y_pred[:, i] == 0)).sum()
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
        print(f"  {label:<25} precision={precision:.2f}  recall={recall:.2f}")

    # Save model and metadata
    model_dir = os.path.join(os.path.dirname(__file__), 'model_data')
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, 'advisor_model.pkl')
    meta_path  = os.path.join(model_dir, 'model_meta.pkl')

    joblib.dump(model, model_path)
    joblib.dump({'feature_names': FEATURE_NAMES, 'rec_labels': REC_LABELS}, meta_path)

    print(f"\nModel saved to:    {model_path}")
    print(f"Metadata saved to: {meta_path}")
    print("Training complete!")


if __name__ == '__main__':
    train_and_save()