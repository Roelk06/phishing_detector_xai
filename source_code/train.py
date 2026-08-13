import pandas as pd
import xgboost as xgb
import shap
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from source_code.feature_extraction import FeatureExtractor

def process_data():
    try:
        df = pd.read_csv("data/url_dataset.csv")
    except FileNotFoundError:
        print("Dataset not found.")
        return None

    extractor = FeatureExtractor()
    feature_list = []

    for index, row in df.iterrows():
        url = row["url"]
        features = extractor.extract_features(url)
        features["is_phishing"] = row["is_phishing"]
        feature_list.append(features)

    return pd.DataFrame(feature_list)

def train_model():
    df = process_data()
    if df is None:
        return

    X = df.drop(columns=['is_phishing'])
    y = df['is_phishing']

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {'max_depth': [3, 4, 5], 'learning_rate': [0.01, 0.1, 0.2], 'n_estimators': [50, 100, 200]}

    base_model = xgb.XGBClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=base_model, param_grid=param_grid, cv=3, scoring="accuracy", verbose=1)
    grid_search.fit(x_train, y_train)

    best_model = grid_search.best_estimator_
    predictions = best_model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Best Model Accuracy: {accuracy * 100:.2f}%")

    explainer = shap.TreeExplainer(best_model)

    best_model.save_model("models/xgboost_grid_search_model.json")
    with open("models/shap_explainer.pkl", "wb") as f:
        pickle.dump(explainer, f)

if __name__ == "__main__":
    train_model()
    


