import streamlit as st
import xgboost as xgb
import pandas as pd
import shap
import pickle
import matplotlib.pyplot as plt
from source_code.feature_extraction import FeatureExtractor

@st.cache_resource
def load_models():

    model = xgb.XGBClassifier()
    model.load_model("models/xgb_model.json")

    with open("models/explainer.pkl", "rb") as f:
        explainer = pickle.load(f)

    feature_extractor = FeatureExtractor()
    return model, explainer, feature_extractor

model, explainer, feature_extractor = load_models()

st.set_page_config(page_title = "XAI phishing detector", page_icon = "🕵️‍♂️")
st.title("🕵️‍♂️ XAI phishing detector")
st.markdown("Enter a URL or Email to analyze its threat level and see the reasoning behind the prediction.")

user_input = st.text_input("URL / Email to check:", placeholder="e.g., https://github.com")

if st.button("Analyze link") and user_input:
    with st.spinner("Analyzing..."):

        features_dict = feature_extractor.extract_features(user_input)
        features_df = pd.DataFrame([features_dict])

        probabilities = model.predict_proba(features_df)[0]
        phishing_probability = probabilities[1] * 100

        st.markdown("---")
        if phishing_probability > 50:
            st.error(f"⚠️ This is phishing!!! ({phishing_probability:.2f}%)")
        else:
            st.success(f"✅ This is not phishing. ({phishing_probability:.2f}%)")

        st.markdown("Feature breakdown:")
        st.write(features_df)

        st.markdown("Why did the model make this decision?")
        st.caption("Red arrows push the model towards phishing, while blue arrows push it towards not phishing.")

        shap_values = explainer(features_df)

        fig, ax = plt.subplots(figsize=(10, 4))
        shap.plots.waterfall(shap_values[0], show=False)

        st.pyplot(fig)

