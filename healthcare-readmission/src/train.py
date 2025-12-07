# src/train.py
import os
from .preprocess import load_data, basic_preprocess
from .model import train_models
from sklearn.model_selection import train_test_split

os.makedirs('models', exist_ok=True)

if __name__ == "__main__":
    df = load_data('data/train.csv')
    X, y, imputer, scaler = basic_preprocess(df, target_col='readmitted')
    X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    # Save transformers
    import joblib
    joblib.dump(imputer, 'models/imputer.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    rf, xgb = train_models(X_tr, y_tr, X_val, y_val, save_path='models/')
