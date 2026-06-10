import streamlit as st
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

st.title("Student Performance Predictor")

gender = st.selectbox("Gender", ["male", "female"])

race_ethnicity = st.selectbox(
    "Race/Ethnicity",
    [
        "group A",
        "group B",
        "group C",
        "group D",
        "group E"
    ]
)

parental_level_of_education = st.selectbox(
    "Parental Level of Education",
    [
        "associate's degree",
        "bachelor's degree",
        "high school",
        "master's degree",
        "some college",
        "some high school"
    ]
)

lunch = st.selectbox(
    "Lunch",
    ["standard", "free/reduced"]
)

test_preparation_course = st.selectbox(
    "Test Preparation Course",
    ["none", "completed"]
)

reading_score = st.number_input(
    "Reading Score",
    min_value=0,
    max_value=100,
    value=50
)

writing_score = st.number_input(
    "Writing Score",
    min_value=0,
    max_value=100,
    value=50
)

if st.button("Predict"):

    data = CustomData(
        gender=gender,
        race_ethnicity=race_ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score
    )

    pred_df = data.get_data_as_dataframe()

    predict_pipeline = PredictPipeline()
    result = predict_pipeline.predict(pred_df)

    st.success(f"Predicted Math Score: {result[0]:.2f}")
