import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

from auth import register_user, login_user
from db import history_collection

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Student Performance Predictor", layout="wide")

# ── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

# ── Train model (done once, reused everywhere) ────────────────────────────────
@st.cache_resource
def load_model():
    """
    Trains a simple LinearRegression on a small hard-coded dataset.
    Features: [study_hours, sleep_hours, attendance, screen_time, previous_marks]
    """
    X = np.array([
        [2,  5, 60, 6, 40],
        [4,  6, 70, 5, 50],
        [6,  7, 80, 4, 60],
        [8,  7, 85, 3, 70],
        [10, 8, 90, 2, 80],
    ])
    y = np.array([40, 55, 65, 75, 90])
    m = LinearRegression()
    m.fit(X, y)
    return m

model = load_model()

# ══════════════════════════════════════════════════════════════════════════════
# AUTH PAGES  (shown only when no user is logged in)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.user is None:

    st.title("🎓 Student Performance Predictor")
    st.caption("Log in or create an account to get started.")

    # Register tab comes first so new users don't hit "Invalid credentials"
    tab_register, tab_login = st.tabs(["📝 Register", "🔐 Login"])

    # ── Register ──────────────────────────────────────────────────────────────
    with tab_register:
        st.subheader("Create an Account")
        new_user = st.text_input("Choose a Username", key="reg_user")
        new_pass = st.text_input("Choose a Password", type="password", key="reg_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register", use_container_width=True):
            if not new_user or not new_pass:
                st.error("Username and password cannot be empty.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                success = register_user(new_user, new_pass)
                if success:
                    st.success("✅ Account created! Switch to the Login tab to sign in.")
                else:
                    st.error("❌ Username already taken. Please choose another.")

    # ── Login ─────────────────────────────────────────────────────────────────
    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.error("Please enter both username and password.")
            elif login_user(username, password):
                st.session_state.user = username
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please register first if you don't have an account.")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP  (shown only after login)
# ══════════════════════════════════════════════════════════════════════════════
else:
    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/student-male--v1.png", width=64)
        st.markdown(f"### 👋 Hi, **{st.session_state.user}**")
        st.divider()
        page = st.radio("Navigate", ["🔮 Predict", "📊 Dashboard"])
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # PREDICT PAGE
    # ══════════════════════════════════════════════════════════════════════════
    if page == "🔮 Predict":
        st.title("🔮 Predict Your Marks")
        st.caption("Fill in your details below and click **Predict** to see your estimated score.")

        st.divider()

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("#### 📚 Academic Inputs")
            study_hours   = st.slider("Daily Study Hours",     min_value=0.0, max_value=12.0, value=4.0, step=0.5)
            attendance    = st.slider("Attendance (%)",        min_value=0,   max_value=100,  value=75)
            previous_marks = st.slider("Previous Exam Marks", min_value=0,   max_value=100,  value=60)

        with col2:
            st.markdown("#### 🌙 Lifestyle Inputs")
            sleep_hours  = st.slider("Daily Sleep Hours",  min_value=0.0, max_value=12.0, value=7.0, step=0.5)
            screen_time  = st.slider("Daily Screen Time (hrs)", min_value=0.0, max_value=12.0, value=3.0, step=0.5)

        st.divider()

        if st.button("🚀 Predict My Marks", use_container_width=True, type="primary"):
            input_data = np.array([[study_hours, sleep_hours, attendance, screen_time, previous_marks]])
            pred = float(model.predict(input_data)[0])
            pred = max(0.0, min(100.0, pred))   # clamp to [0, 100]

            # ── Result card ───────────────────────────────────────────────────
            st.divider()
            grade_col, advice_col = st.columns([1, 2], gap="large")

            with grade_col:
                if pred >= 75:
                    st.metric("🎯 Predicted Score", f"{pred:.1f} / 100")
                    st.success("🔥 **Excellent!** Keep it up!")
                elif pred >= 50:
                    st.metric("🎯 Predicted Score", f"{pred:.1f} / 100")
                    st.warning("⚡ **Good effort!** A bit more focus will get you there.")
                else:
                    st.metric("🎯 Predicted Score", f"{pred:.1f} / 100")
                    st.error("⚠️ **Needs improvement.** Don't give up — consistency is key!")

            with advice_col:
                st.markdown("#### 💡 Personalised Tips")
                tips = []
                if study_hours < 4:
                    tips.append("📖 Try to study at least **4–5 hours** daily.")
                if sleep_hours < 6:
                    tips.append("😴 Aim for **7–8 hours** of sleep for better retention.")
                if attendance < 75:
                    tips.append("🏫 Attendance below 75% can impact your final grade significantly.")
                if screen_time > 5:
                    tips.append("📵 Reduce screen time to less than **3 hours** to stay focused.")
                if previous_marks < 50:
                    tips.append("📝 Review past topics and practise more mock tests.")

                if tips:
                    for tip in tips:
                        st.markdown(f"- {tip}")
                else:
                    st.markdown("✅ Your habits look great! Stay consistent.")

            # ── Save to MongoDB ───────────────────────────────────────────────
            history_collection.insert_one({
                "user":           st.session_state.user,
                "study_hours":    study_hours,
                "sleep_hours":    sleep_hours,
                "attendance":     attendance,
                "screen_time":    screen_time,
                "previous_marks": previous_marks,
                "predicted":      pred,
                "time":           datetime.now(),
            })

    # ══════════════════════════════════════════════════════════════════════════
    # DASHBOARD PAGE
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📊 Dashboard":
        st.title("📊 Your Performance Dashboard")
        st.caption("All your past predictions are shown here.")

        raw = list(history_collection.find({"user": st.session_state.user}))

        if not raw:
            st.info("No predictions yet. Head to the **Predict** page to get started!")
        else:
            df = pd.DataFrame(raw)
            df.drop(columns=["_id", "user"], inplace=True, errors="ignore")
            df["time"] = pd.to_datetime(df["time"]).dt.strftime("%d %b %Y, %H:%M")
            df.rename(columns={
                "study_hours":    "Study Hrs",
                "sleep_hours":    "Sleep Hrs",
                "attendance":     "Attendance %",
                "screen_time":    "Screen Time Hrs",
                "previous_marks": "Prev. Marks",
                "predicted":      "Predicted Score",
                "time":           "Date & Time",
            }, inplace=True)

            # ── Summary stats ─────────────────────────────────────────────────
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Predictions", len(df))
            m2.metric("Best Score",        f"{df['Predicted Score'].max():.1f}")
            m3.metric("Average Score",     f"{df['Predicted Score'].mean():.1f}")

            st.divider()

            # ── Progress chart ────────────────────────────────────────────────
            st.subheader("📈 Score Over Time")
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.plot(df["Predicted Score"].values, marker="o", linewidth=2, color="#4F8BF9")
            ax.fill_between(range(len(df)), df["Predicted Score"].values, alpha=0.15, color="#4F8BF9")
            ax.set_ylabel("Predicted Score")
            ax.set_xlabel("Attempt #")
            ax.set_title("Your Performance Over Time")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            st.pyplot(fig)

            st.divider()

            # ── Raw history table ─────────────────────────────────────────────
            st.subheader("🗂️ Full History")
            st.dataframe(df, use_container_width=True, hide_index=True)
