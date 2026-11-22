
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Medical Insurance Cost Forecaster",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Insurance Cost Forecaster")
st.write("Predict your estimated medical insurance cost using Machine Learning.")

@st.cache_resource
def load_model():
    return joblib.load("insurance_model.pkl")

try:
    model = load_model()

    st.subheader("Enter Your Information")

    age = st.number_input("Age", min_value=1, max_value=100, value=30)

    gender = st.selectbox("Gender", ["male", "female"])

    height_feet = st.number_input("Height (Feet)", min_value=0, max_value=8, value=5)

    height_inches = st.number_input("Additional Inches", min_value=0, max_value=11, value=6)

    weight = st.number_input("Weight (KG)", min_value=1.0, value=70.0)

    children = st.number_input("Number of Children", min_value=0, max_value=20, value=1)

    smoker = st.selectbox("Are You a Smoker?", ["no", "yes"])

    region = st.selectbox(
        "Region",
        ["northeast", "northwest", "southeast", "southwest"]
    )

    if st.button("Predict Insurance Cost", type="primary"):

        height_meters = (height_feet * 12 + height_inches) * 0.0254

        if height_meters <= 0:
            st.error("Please enter a valid height.")

        else:
            bmi = weight / (height_meters ** 2)

            user_data = pd.DataFrame({
                "age": [age],
                "sex": [gender],
                "bmi": [bmi],
                "children": [children],
                "smoker": [smoker],
                "region": [region]
            })

            prediction = model.predict(user_data)[0]

            st.success("Prediction Completed!")

            st.metric("Your Calculated BMI", f"{bmi:.2f}")

            st.metric(
                "Estimated Insurance Cost",
                f"${prediction:,.2f}"
            )

            st.info("This is an AI-based estimate, not an actual insurance quote.")

except FileNotFoundError:
    st.error("Model file not found. Please upload insurance_model.pkl to your repository.")


