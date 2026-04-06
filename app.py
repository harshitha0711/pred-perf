import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

st.title("🎓 AI Student Performance Analyzer")
st.write("Predict and improve your academic performance using Machine Learning")


st.header("📥 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input("Study Hours (per day)", 0.0, 12.0, step=0.5)
    attendance = st.number_input("Attendance (%)", 0, 100)

with col2:
    sleep_hours = st.number_input("Sleep Hours (per day)", 0.0, 12.0, step=0.5)
    screen_time = st.number_input("Screen Time (hours/day)", 0.0, 12.0, step=0.5)

previous_marks = st.number_input("Previous Exam Marks", 0, 100)


X = np.array([
    [2, 5, 60, 6, 40],
    [4, 6, 70, 5, 50],
    [6, 7, 80, 4, 60],
    [8, 7, 85, 3, 70],
    [10, 8, 90, 2, 80]
])

y = np.array([40, 55, 65, 75, 90])

model = LinearRegression()
model.fit(X, y)


if st.button("🚀 Predict Marks"):
    input_data = np.array([[study_hours, sleep_hours, attendance, screen_time, previous_marks]])
    predicted_marks = model.predict(input_data)[0]

    st.subheader("📊 Predicted Marks")
    st.success(f"🎯 {predicted_marks:.2f} marks")

    
    st.subheader("💡 Study Suggestions")

    if predicted_marks < 50:
        st.error("⚠️ You need serious improvement!")
        st.write("👉 Study at least 6–8 hours daily")
        st.write("👉 Reduce screen time")
        st.write("👉 Maintain 7–8 hours of sleep")
        st.write("👉 Focus on weak subjects")

    elif predicted_marks < 75:
        st.warning("⚡ You're doing okay, but can improve!")
        st.write("👉 Revise daily")
        st.write("👉 Practice previous papers")
        st.write("👉 Improve consistency")

    else:
        st.success("🔥 Excellent performance!")
        st.write("👉 Maintain your routine")
        st.write("👉 Try advanced problems")
        st.write("👉 Help others (teaching improves mastery)")

    
    st.subheader("📌 Prediction Explanation")

    st.write(f"""
    - 📚 Study Hours: {study_hours} hrs/day  
    - 😴 Sleep Hours: {sleep_hours} hrs/day  
    - 📊 Attendance: {attendance}%  
    - 📱 Screen Time: {screen_time} hrs/day  
    - 📝 Previous Marks: {previous_marks}  

    These factors combined influenced your predicted score.
    """)


st.header("📈 Performance Analysis")

if st.button("Show Graphs"):
    x = [2, 4, 6, 8, 10]
    y = [40, 55, 65, 75, 90]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("Study Hours")
    ax.set_ylabel("Marks")
    ax.set_title("Study Hours vs Marks")

    st.pyplot(fig)