# src/preprocess.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def load_data(path):
    df = pd.read_csv(path)
    return df

def basic_preprocess(df, target_col='readmitted'):
    # Drop obvious ID cols if any
    if 'patient_id' in df.columns:
        df = df.drop('patient_id', axis=1)
    # Separate X,y
    y = df[target_col].map({0:0, 1:1})  # ensure numeric
    X = df.drop(columns=[target_col])
    # Simple impute
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_imputed), columns=X.columns)
    return X_scaled, y, imputer, scaler
