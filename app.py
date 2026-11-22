
import streamlit as st
import pandas as pd
import joblib

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Medical Insurance Cost Forecaster",
    page_icon="🏥",
    layout="wide"
)

# Approximate USD to BDT exchange rate
# Update this rate when needed.
USD_TO_BDT = 124.73

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f9ff, #edf4ff);
    }

    .main .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #123c69, #2563eb);
        padding: 35px 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(37,99,235,0.18);
    }

    .hero h1 {
        color: white;
        font-size: 32px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #e5efff;
        font-size: 16px;
    }

    .section-title {
        color: #123c69;
        font-size: 22px;
        font-weight: 700;
        margin: 15px 0;
    }

    .result-note {
        background: #e8f1ff;
        border-left: 4px solid #2563eb;
        padding: 14px;
        border-radius: 8px;
        color: #123c69;
        margin-top: 15px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# LANGUAGE SELECTION
# =====================================

language = st.radio(
    "🌐 Language / ভাষা",
    ["বাংলা", "English"],
    horizontal=True
)

if language == "বাংলা":

    t = {
        "title": "মেডিকেল ইন্স্যুরেন্স কস্ট ফোরকাস্টার",
        "subtitle": "Machine Learning ব্যবহার করে আনুমানিক Insurance Cost জানুন",
        "form": "আপনার তথ্য দিন",
        "age": "আপনার বয়স",
        "gender": "লিঙ্গ",
        "male": "পুরুষ",
        "female": "নারী",
        "height": "উচ্চতা",
        "feet": "ফুট",
        "inches": "ইঞ্চি",
        "weight": "ওজন (কেজি)",
        "children": "সন্তানের সংখ্যা",
        "smoker": "আপনি কি ধূমপান করেন?",
        "yes": "হ্যাঁ",
        "no": "না",
        "region": "অঞ্চল",
        "predict": "ইন্স্যুরেন্স খরচ অনুমান করুন",
        "result": "আপনার Prediction Result",
        "bmi": "আপনার BMI",
        "cost": "আনুমানিক Insurance Cost",
        "success": "Prediction সফল হয়েছে!",
        "disclaimer": "এটি একটি Machine Learning ভিত্তিক আনুমানিক ফলাফল। এটি প্রকৃত Insurance Quote নয়।",
        "rate": "আনুমানিক বিনিময় হার",
        "footer": "Developed with Machine Learning",
        "northeast": "উত্তর-পূর্ব",
        "northwest": "উত্তর-পশ্চিম",
        "southeast": "দক্ষিণ-পূর্ব",
        "southwest": "দক্ষিণ-পশ্চিম",
        "bmi_category": "BMI ক্যাটাগরি"
    }

else:

    t = {
        "title": "Medical Insurance Cost Forecaster",
        "subtitle": "Estimate your insurance cost using Machine Learning",
        "form": "Enter Your Information",
        "age": "Your Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "height": "Height",
        "feet": "Feet",
        "inches": "Inches",
        "weight": "Weight (KG)",
        "children": "Number of Children",
        "smoker": "Are You a Smoker?",
        "yes": "Yes",
        "no": "No",
        "region": "Region",
        "predict": "Predict Insurance Cost",
        "result": "Your Prediction Result",
        "bmi": "Your BMI",
        "cost": "Estimated Insurance Cost",
        "success": "Prediction Completed Successfully!",
        "disclaimer": "This is a Machine Learning estimate, not an actual insurance quote.",
        "rate": "Approximate Exchange Rate",
        "footer": "Developed with Machine Learning",
        "northeast": "Northeast",
        "northwest": "Northwest",
        "southeast": "Southeast",
        "southwest": "Southwest",
        "bmi_category": "BMI Category"
    }

# =====================================
# HEADER
# =====================================

st.markdown(
    f"""
    <div class="hero">
        <h1>🏥 {t['title']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# LOAD TRAINED MODEL
# =====================================

@st.cache_resource
def load_model():
    return joblib.load("insurance_model.pkl")

try:
    model = load_model()
except Exception:
    st.error(
        "Model could not be loaded. Please check the model file "
        "and deployment logs."
    )
    st.stop()

# =====================================
# INPUT FORM
# =====================================

st.markdown(
    f'<div class="section-title">📋 {t["form"]}</div>',
    unsafe_allow_html=True
)

with st.form("insurance_form"):

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            t["age"],
            min_value=1,
            max_value=100,
            value=30
        )

        gender_label = st.selectbox(
            t["gender"],
            [t["male"], t["female"]]
        )

        st.write(t["height"])

        h1, h2 = st.columns(2)

        with h1:
            height_feet = st.number_input(
                t["feet"],
                min_value=1,
                max_value=8,
                value=5
            )

        with h2:
            height_inches = st.number_input(
                t["inches"],
                min_value=0,
                max_value=11,
                value=6
            )

        weight = st.number_input(
            t["weight"],
            min_value=1.0,
            max_value=300.0,
            value=70.0,
            step=0.5
        )

    with col2:

        children = st.number_input(
            t["children"],
            min_value=0,
            max_value=20,
            value=1
        )

        smoker_label = st.selectbox(
            t["smoker"],
            [t["no"], t["yes"]]
        )

        region_labels = [
            t["northeast"],
            t["northwest"],
            t["southeast"],
            t["southwest"]
        ]

        region_label = st.selectbox(
            t["region"],
            region_labels
        )

    submitted = st.form_submit_button(
        f"🔍 {t['predict']}",
        use_container_width=True,
        type="primary"
    )

# =====================================
# PREDICTION
# =====================================

if submitted:

    height_meters = (
        height_feet * 12 + height_inches
    ) * 0.0254

    if height_meters <= 0:

        st.error("Please enter a valid height.")

    else:

        bmi = weight / (height_meters ** 2)

        gender = (
            "male" if gender_label == t["male"]
            else "female"
        )

        smoker = (
            "yes" if smoker_label == t["yes"]
            else "no"
        )

        region_mapping = {
            t["northeast"]: "northeast",
            t["northwest"]: "northwest",
            t["southeast"]: "southeast",
            t["southwest"]: "southwest"
        }

        region = region_mapping[region_label]

        user_data = pd.DataFrame({
            "age": [age],
            "sex": [gender],
            "bmi": [bmi],
            "children": [children],
            "smoker": [smoker],
            "region": [region]
        })

        try:

            prediction = float(
                model.predict(user_data)[0]
            )

            prediction_bdt = prediction * USD_TO_BDT

            st.markdown("---")

            st.markdown(
                f'<div class="section-title">📊 {t["result"]}</div>',
                unsafe_allow_html=True
            )

            st.success(t["success"])

            result1, result2, result3 = st.columns(3)

            with result1:
                st.metric(
                    t["bmi"],
                    f"{bmi:.2f}"
                )

            with result2:
                st.metric(
                    "Estimated Cost (USD)",
                    f"${prediction:,.2f}"
                )

            with result3:
                st.metric(
                    "আনুমানিক খরচ (BDT)" if language == "বাংলা"
                    else "Estimated Cost (BDT)",
                    f"৳{prediction_bdt:,.2f}"
                )

            st.info(
                f"{t['rate']}: 1 USD ≈ ৳{USD_TO_BDT:.2f}"
            )

            st.markdown(
                f"""
                <div class="result-note">
                    <b>⚠️ {t['disclaimer']}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:

            st.error(
                "Prediction failed. Please check your model and input data."
            )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align:center; color:#64748b; padding:15px;">
        🏥 <b>Medical Insurance Cost Forecaster</b><br>
        {t['footer']}<br>
        © 2026 All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)



