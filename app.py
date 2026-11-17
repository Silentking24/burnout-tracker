import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os
import csv


# --- PAGE CONFIG ---
st.set_page_config(page_title="Healthcare Worker Burnout Tracker",
                   page_icon="📊", layout="centered")

st.title("🏥 Healthcare Worker Management System")
st.write("Track your operational stressors, review localized risk scores, and monitor your longitudinal trajectory. ")

# --- SIDEBAR NAVIGATION ---
menu = st.sidebar.selectbox(
    "Select Action", ["Log New Assessment", "View Trajectory Chart"])

# --- CORE FUNCTIONS (Same as your script) ---


def calculate_burnout_risk(hours, raw_stress, emotional_indicators, physical_indicators, vacation_days, support_score):
    base_score = (hours * 0.4) + (raw_stress * 5.0) + \
        (emotional_indicators * 3.0) + (physical_indicators * 2.0)
    mitigation = (vacation_days * 2.0) + (support_score * 1.5)
    final_score = round(max(0, min(100, base_score - mitigation)), 1)

    if final_score >= 75:
        risk_tier = "High Risk"
    elif final_score >= 50:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low/ Managed Risk"

    return final_score, risk_tier


def log_session_to_csv(score, tier):
    file_name = "burnout_history.csv"
    file_exists = os.path.isfile(file_name)
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Burnout Index Score",
                            "Assigned Operational Tier"])
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        writer.writerow([current_date, score, tier])


# --- APP WORKFLOW: LOG NEW ASSESSMENT ---
if menu == "Log New Assessment":
    st.header("Weekly Assessment Intake")

    with st.form("burnout_form"):
        hours = st.number_input(
            "Average clinical/administrative hours worked this week:", min_value=0.0, max_value=120.0, value=40.0)
        raw_stress = st.slider(
            "Rate clinical acute stress level:", min_value=1.0, max_value=10.0, value=5.0)

        st.subheader("Emotional Symptoms Checklist")
        emotions = ['Sadness or Hopelessness', 'Extreme Irritability or Short Fuse',
                    'Anxiety and Excessive Worrying', 'Loss Of Motivation or Anhedonia', 'Feeling Overwhelmed']
        emotional_count = 0
        for emotion in emotions:
            if st.checkbox(emotion, key=f"emo{emotion}"):
                emotional_count += 1

        st.subheader("Physical Symptoms Checklist")
        physical = ['Fatigue and Low Energy', 'Headaches or Tension', 'Muscle Tension or Pain',
                    'Sleep Disturbances', 'Shortness of Breath or Rapid Heartbeat']
        physical_count = 0
        for symptom in physical:
            if st.checkbox(symptom, key=f"phys_{symptom}"):
                physical_count += 1

        vacation_days = st.number_input(
            "Days of restorative time off taken in past 30 days:", min_value=0, max_value=30, value=0)
        support_score = st.slider(
            "Rate workplace organizational peer support:", min_value=1.0, max_value=10.0, value=5.0)

        submitted = st.form_submit_button("Calculate Burnout Index & Log")

        if submitted:
            score, tier = calculate_burnout_risk(
                hours, raw_stress, emotional_count, physical_count, vacation_days, support_score)
            log_session_to_csv(score, tier)

            st.success("Session securely logged!")
            st.metric(label="Calculated Burnout Index",
                      value=f"{score} / 100", delta=tier)

            if tier == "High Risk":
                st.error(
                    "Action Needed: Immediate decompression and schedule adjustments recommended.")
            elif tier == "Moderate Risk":
                st.warning(
                    "Precautionary: Monitor shifts and focus on utilizing available support network.")
            else:
                st.info(
                    "Sustained Status: Maintain health boundary setting and routine off-time.")

    # --- APP WORKFLOW: VIEW CHART ---
elif menu == "View Trajectory Chart":
    st.header("Longitudinal Trajectory Analysis")

    if not os.path.exists("burnout_history.csv"):
        st.warning("⚠️ No tracking history found yet. Log an assessment first!")
    else:
        dates = []
        scores = []

        try:
            with open("burnout_history.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        try:
                            d = datetime.datetime.strptime(
                                row[0].strip(), "%Y-%m-%d")
                            s = float(row[1].strip())
                            dates.append(d)
                            scores.append(s)
                        except ValueError:
                            continue
        except Exception as e:
            st.error(f"Error reading histroy file: {e}")

        if not dates or not scores:
            st.info("ℹ️ No valid data entries available to plot yet.")
        else:
            # Sort data chronologically to ensure clean trajectory lines
            combined = sorted(zip(dates, scores))
            dates, scores = zip(*combined)
            dates = list(dates)
            scores = list(scores)

            # Calculate 4-session moving average for smoother trajectory trend
            window_size = min(4, len(scores))
            moving_avg = []
            for i in range(len(scores)):
                window = scores[max(0, i - window_size + 1):i + 1]
                moving_avg.append(sum(window) / len(window))

            # Render the matplotlib plot inside Streamlit
            fig, ax = plt.subplots(figsize=(10, 5))

# Plot raw scores with lighter markers and smoothed trend line
            ax.plot(dates, scores, marker='o', linestyle='-',
                    color='#b0c4de', linewidth=1.5, label='Raw Weekly Index')
            ax.plot(dates, moving_avg, color='#1f77b4', linewidth=3.0,
                    label=f'Trajectory Trend ({window_size}-Session Avg)')

            # Risk Threshold Guidelines
            ax.axhline(y=75, color='#d9534f', linestyle='--',
                       label='High Risk (>= 75)')
            ax.axhline(y=50, color='#f0ad4e', linestyle='--',
                       label='Moderate Risk (>=50)')

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
            fig.autofmt_xdate()
            ax.set_ylim(0, 105)
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend(loc='upper left', frameon=True)
            ax.set_ylabel("Burnout Score (0-100)")
            ax.set_xlabel("Date")
            ax.set_title("Healthcare Worker Burnout Trajectory Analysis",
                         fontsize=12, fontweight='bold')

            st.pyplot(fig)
