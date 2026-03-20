"""
train_model.py
──────────────
Standalone script to train and save the ML models.
Run once before starting the Flask app:
    python train_model.py

In production, replace synthetic data with:
  - PhishTank dataset  (https://www.phishtank.com/developer_info.php)
  - APKID dataset      (https://github.com/rednaga/APKiD)
  - Kaggle Phishing URL dataset
"""
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model  import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

np.random.seed(42)
N = 5000

# ─── URL DATASET ─────────────────────────────────────────────
def generate_url_data():
    # Genuine
    genuine = np.column_stack([
        np.random.randint(15, 60, N//2),
        np.random.randint(0, 3, N//2),
        np.random.randint(1, 3, N//2),
        np.random.randint(0, 2, N//2),
        np.ones(N//2),
        np.zeros(N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(0, 2, N//2),
        np.zeros(N//2),
        np.random.randint(0, 3, N//2),
        np.random.randint(0, 2, N//2),
        np.random.uniform(3.0, 4.5, N//2),
        np.zeros(N//2),
        np.zeros(N//2),
        np.random.randint(5, 20, N//2),
    ])
    # Fake
    fake = np.column_stack([
        np.random.randint(80, 300, N//2),
        np.random.randint(5, 20, N//2),
        np.random.randint(3, 8, N//2),
        np.random.randint(3, 10, N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(2, 5, N//2),
        np.random.randint(3, 8, N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(3, 8, N//2),
        np.ones(N//2),
        np.random.uniform(4.5, 6.0, N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(0, 2, N//2),
        np.random.randint(20, 60, N//2),
    ])
    X = np.vstack([genuine, fake])
    y = np.array([0]*(N//2) + [1]*(N//2))
    return X, y

print("Training URL model...")
X_url, y_url = generate_url_data()
scaler_url   = StandardScaler()
X_url_scaled = scaler_url.fit_transform(X_url)
X_tr, X_te, y_tr, y_te = train_test_split(X_url_scaled, y_url, test_size=0.2, random_state=42)

clf_url = RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42, n_jobs=-1)
clf_url.fit(X_tr, y_tr)
print(f"  URL Model Accuracy: {accuracy_score(y_te, clf_url.predict(X_te)):.4f}")
print(classification_report(y_te, clf_url.predict(X_te), target_names=['Genuine','Fake']))

with open(os.path.join(MODEL_DIR, 'url_model.pkl'),  'wb') as f: pickle.dump(clf_url,    f)
with open(os.path.join(MODEL_DIR, 'url_scaler.pkl'), 'wb') as f: pickle.dump(scaler_url, f)
print("  Saved url_model.pkl and url_scaler.pkl\n")

# ─── APK DATASET ─────────────────────────────────────────────
def generate_apk_data():
    genuine = np.column_stack([
        np.random.uniform(1, 80, N//2),
        np.ones(N//2),
        np.ones(N//2),
        np.ones(N//2),
        np.random.randint(0, 5, N//2),
        np.random.randint(3, 15, N//2),
        np.random.randint(0, 3, N//2),
        np.random.randint(19, 28, N//2),
        np.random.randint(30, 33, N//2),
    ])
    fake = np.column_stack([
        np.random.uniform(0.05, 8, N//2),
        np.ones(N//2),
        np.ones(N//2),
        np.ones(N//2),
        np.random.randint(8, 22, N//2),
        np.random.randint(15, 30, N//2),
        np.random.randint(6, 18, N//2),
        np.random.randint(14, 19, N//2),
        np.random.randint(19, 25, N//2),
    ])
    X = np.vstack([genuine, fake])
    y = np.array([0]*(N//2) + [1]*(N//2))
    return X, y

print("Training APK model...")
X_apk, y_apk = generate_apk_data()
scaler_apk   = StandardScaler()
X_apk_scaled = scaler_apk.fit_transform(X_apk)
X_tr, X_te, y_tr, y_te = train_test_split(X_apk_scaled, y_apk, test_size=0.2, random_state=42)

clf_apk = RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42, n_jobs=-1)
clf_apk.fit(X_tr, y_tr)
print(f"  APK Model Accuracy: {accuracy_score(y_te, clf_apk.predict(X_te)):.4f}")
print(classification_report(y_te, clf_apk.predict(X_te), target_names=['Genuine','Fake']))

with open(os.path.join(MODEL_DIR, 'apk_model.pkl'),  'wb') as f: pickle.dump(clf_apk,    f)
with open(os.path.join(MODEL_DIR, 'apk_scaler.pkl'), 'wb') as f: pickle.dump(scaler_apk, f)
print("  Saved apk_model.pkl and apk_scaler.pkl\n")

print("✅ All models trained and saved successfully!")
print("   Next step: python app.py")
