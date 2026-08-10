import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def mock_data():

    np.random.seed(42)
    # 1. Generate 500 'Legitimate' URLs
    legit = pd.DataFrame({
        'is_email': np.random.choice([0, 1], 500, p=[0.9, 0.1]),
        'input_length': np.random.normal(25, 5, 500),
        'domain_length': np.random.normal(12, 3, 500),
        'dot_count': np.random.poisson(1, 500),
        'hyphen_count': np.random.poisson(0.2, 500),
        'apenstaartje_count': np.random.poisson(0, 500),
        'digit_count': np.random.poisson(1, 500),
        'domain_entropy': np.random.normal(3.0, 0.5, 500),
        'domain_age': np.random.normal(3000, 1000, 500),
        'is_phishing': 0  # Our target variable (0 = Safe)
    })
    
    # 2. Generate 500 'Phishing' URLs
    phish = pd.DataFrame({
        'is_email': np.random.choice([0, 1], 500, p=[0.7, 0.3]),
        'input_length': np.random.normal(55, 15, 500),
        'domain_length': np.random.normal(20, 5, 500),
        'dot_count': np.random.poisson(3, 500),
        'hyphen_count': np.random.poisson(2, 500),
        'apenstaartje_count': np.random.poisson(0.5, 500),
        'digit_count': np.random.poisson(8, 500),
        'domain_entropy': np.random.normal(4.5, 0.4, 500),
        'domain_age': np.random.choice([-1, 10, 50], 500), # Notice the -1s!
        'is_phishing': 1  # Our target variable (1 = Phishing)
    })
    
    return pd.concat([legit, phish], ignore_index=True)

def train_model():
    print("generating training data...")
    data = mock_data()

    X = data.drop(columns=['is_phishing'])
    y = data['is_phishing']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("training model...")
    model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    print("Setting up explainer...")
    explainer = shap.TreeExplainer(model)

    print("Saving model and explainer...")
    model.save_model("models/xgb_model.json")

    with open("models/explainer.pkl", "wb") as f:
        pickle.dump(explainer, f)

    print("Training is done!")

if __name__ == "__main__":
    train_model()
    


