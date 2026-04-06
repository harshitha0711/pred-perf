import streamlit as st
from model import predict_marks

st.title("🎓 Student Performance Predictor")

hours = st.slider("Study Hours", 0, 12)
sleep = st.slider("Sleep Hours", 0, 12)

if st.button("Predict"):
    result = predict_marks(hours, sleep)
    st.success(f"Predicted Marks: {result:.2f}")