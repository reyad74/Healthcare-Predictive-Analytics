# src/model.py
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_models(X_train, y_train, X_val, y_val, save_path='models/'):
    rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    xgb = XGBClassifier(n_estimators=200, use_label_encoder=False, eval_metric='logloss', random_state=42, n_jobs=4)

    rf.fit(X_train, y_train)
    xgb.fit(X_train, y_train)

    # Validation
    for name, model in [('rf', rf), ('xgb', xgb)]:
        preds = model.predict(X_val)
        acc = accuracy_score(y_val, preds)
        print(f"{name} val acc: {acc:.4f}")
        print(classification_report(y_val, preds))

        joblib.dump(model, f"{save_path}{name}.joblib")
    return rf, xgb
