import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import os
import csv
import matplotlib
# <--This line was added to import pyplot and Force backend compatibility
matplotlib.use('TkAgg')
10


def calculate_burnout_risk(hours, raw_stress, emotional_indicators, physical_indicators, vacation_days, support_score):
    """
    Calculate a localized burnout metric based on healthcare worker operational indicators.
    Returns a categorical risk tier and a numerical score out if 100.
    """
    # Baseline calculation translating operational variables to a unified score matrix
    base_score = (hours * 0.4) + (raw_stress * 5.0) + \
        (emotional_indicators * 3.0) + (physical_indicators * 2.0)

    # Modifier mitigating factors (Vacation history and workplace alignment scores)
    mitigation = (vacation_days * 2.0) + (support_score * 1.5)

    # Standardize the final metrics to a definitive ceiling
    final_score = round(max(0, min(100, base_score - mitigation)), 1)

    # Catagorization algorithm tracking threshold boundaries
    if final_score >= 75:
        risk_tier = "High Risk"
    elif final_score >= 50:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low / Managed Risk"
    return risk_tier, final_score

# Place-holder for your insight function (ensure yours matches this or contains your specific text)


def display_motivation_insight(risk_tier):
    if risk_tier == "High Risk":
        return "Action Needed: Immediate decompression and schedule adjustments recommended."
    elif risk_tier == "Moderate Risk":
        return "Precautionary: Monitor shifts and focus on utilizing available support network."
    else:
        return "Sustained Status: Maintain healthy boundary settings and routine off-time."


def log_session_to_csv(score, tier):
    """Automatically creates or appends weekly scores to a localized tracking file."""
    file_name = "burnout_history.csv"
    file_exists = os.path.isfile(file_name)

    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write headers if the file is being created for the first time
        if not file_exists:
            writer.writerow(["Date", "Burnout Index Score",
                            "Assigned Operational Tier"])

            # Log the current date, score, and tier
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            writer.writerow([current_date, score, tier])


def inject_behavioral_strategies(risk_tier):
    """Outputs targeted, practical support resources tailored to the clinician's score."""
    resources = {
        "High Risk": [
            "CRITICAL ACTIONS: Schedule a decompression window with your clinical lead or supervisor.",
            "National Frontline Responder Helpline: Call/Text 1-888-409-0141 for specialized support.",
            "Employee Assitance Program (EAP): Contact your internal department line for confidential counseling.",
            "Crisis Support Text Line: Text'HOME' to 741741 to connect with a crisis counselor 24/7."
        ],
        "Moderate Risk": [
            "PRECAUTIONARY ACTION: Implement a hard boundary on off-duty charting or email administrative hours.",
            "Peer Support Network: Tap into local clinician roundtables or regional peer group.",
            "Mindful Decompression: Utilize tools like Insight Timer, Medito, Healthy Minds Program.",
            "Shift Audit: Review your clincial vs. administrative load over the last 30 days to identify bottlenecks."
        ],
        "Low/Managed Risk": [
            "SUSTAINED STATUS: Maintain your current boundary settings and protective routines.",
            "Proactive Resilience: Keep prioritizing restorative off-time and scheduling vacations days.",
            "Reflections: Take note of what organizational support structures worked well for you this week."
        ]
    }
    # Safely fetch the matching list or fall back to low risk guidelines
    strategies = resources.get(risk_tier, resources["Low/Managed Risk"])
    for strategy in strategies:
        print(strategy)


def run_tracker():
    print("=" * 60)
    print("     HEALTHCARE WORKER BURNOUT TOOLKIT v1.0     ")
    print("=" * 60)
    print(
        f"Session Log Initialization: {datetime.date.today().strftime('%B %d, %Y')}\n")

    # Operational Data Intake Streams
    try:
        hours = float(
            input("Enter average clinical/administrative hours worked this week: "))
        raw_stress = float(
            input("Rate clinical acute stress level (Scale 1 - 10): "))
    # --- EMOTIONAL SYMPTOMS CHECKLIST---
        emotions = [
            'Sadness or Hopelessness',
            'Extreme irritability or Short fuse',
            'Anxiety and Excessive Worrying',
            'Loss of Motivation or Anhedonia',
            'Feeling Overwhelmed'
        ]
        print("\n---EMOTIONAL SYMPTOMS CHECKLIST---")
        print("Answer 'y' if present, or press Enter for no:")
        emotional_indicators = 0
        for emotion in emotions:
            response = input(f"  - {emotion}? (y/n): ").strip().lower()
            if response in ['y', 'true', '1']:
                emotional_indicators += 1

    # --- PHYSICAL SYMPTOMS CHECKLIST---
        physical = [
            'Fatigue and Low Energy',
            'Headaches or Tension',
            'Muscle tension or pain',
            'Sleep disturbances',
            'Shortness of breath or Rapid heartbeat'
        ]
        print("\n---PHYSICAL SYMPTOMS CHECKLIST---")
        print("Answer 'y' if present, or press Enter for no:")
        physical_indicators = 0
        for symptom in physical:
            response = input(f"  - {symptom}? (y/n): ").strip().lower()
            if response in ['y', 'yes', 'true', '1']:
                physical_indicators += 1

        vacation_days = int(
            input("Days of restorative time off taken in past 30 days: "))
        support_score = float(
            input("Rate workplace organizational peer support (Scale 1 - 10): "))
    except ValueError:
        print("Please enter valid numeric values.")
        return

    # Core Evaluation Computation Engine Call
    risk_tier, exact_score = calculate_burnout_risk(
        hours, raw_stress, emotional_indicators, physical_indicators,
        vacation_days, support_score)
    insight = display_motivation_insight(risk_tier)

    # Display Synthesized Data Report Outputs
    print("\n" + "=" * 40)
    print("       DIAGNOSTIC METRIC SUMMARY      ")
    print("-" * 40)
    print(f"Calculated Burnout Index : {exact_score} / 100")
    print(f"Assigned Operational Tier: ** {risk_tier.upper()} **")
    print("-" * 40)

    # Inject Contextual Behavioral Strategies
    print("\n" + "=" * 40)
    print("STRATEGIC ACTIONABLE RESOURCES")
    print("=" * 40)
    inject_behavioral_strategies(risk_tier)
    print("-" * 40)

    # Trigger the automated data log after the score and tier are calculated.
    log_session_to_csv(exact_score, risk_tier)
    print("Session securely logged to 'burnout_history.csv'.")
    print("=" * 40 + "\n")

    plot_burnout_history()


def plot_burnout_history():
    """Reads the CSV history, filters by time window, calculates moving averages, and renders a focused chart."""
    print("\n--- CHART VIEW OPTIONS ---")
    print("1. Last 30 Days")
    print("2. Last 60 Days")
    print("3. Last 90 Days")
    print("4. All Historical Data")
    choice = input(
        "Select time window for chart (1-4, default is 4): ").strip()

    days_map = {"1": 30, "2": 60, "3": 90}
    max_days = days_map.get(choice, None)

    dates = []
    scores = []

    try:
        with open("burnout_history.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                if len(row) >= 2:
                    entry_date = datetime.datetime.strptime(
                        row[0].strip(), "%Y-%m-%d")
                    entry_score = float(row[1].strip())

                    if max_days:
                        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=max_days)
                        if entry_date >= cutoff_date:
                            dates.append(entry_date)
                            scores.append(entry_score)
                    else:
                        dates.append(entry_date)
                        scores.append(entry_score)
    except FileNotFoundError:
        print("Warning, 'burnout_history.csv' not found yet.")
        return

    if not dates:
        print("Warning, No data entries found within the selected time window.")
        return

    # Calculate 4-session moving average trajectory
    window_size = 4
    moving_avg = []
    for i in range(len(scores)):
        window = scores[max(0, 1 - window_size + 1):i + 1]
        moving_avg.append(sum(window) / len(window))

    # Setting up and rendering the plot
    plt.figure(figsize=(11, 6))

    plt.plot(dates, scores, marker='o', linestyle='-', color='#b0c4de',
             linewidth=1.5, markersize=6, label='Raw Weekly Index')
    plt.plot(dates, moving_avg, color='#1f77b4', linewidth=3.0,
             label=f'Trajectory Trend ({window_size}-Session Avg)')

    plt.axhline(y=75, color='#d9534f', linestyle='--',
                linewidth=1.5, label='High Risk (>=75)')
    plt.axhline(y=50, color='#f0ad4e', linestyle='--',
                linewidth=1.5, label='Moderate Risk (>=50)')

    # ---This will Tighten and Format X-Axis Distinctly---
    ax = plt.gca()
    if len(dates) == 1:
        plt.xlim(dates[0] - datetime.timedelta(days=7),
                 dates[0] + datetime.timedelta(days=7))
    else:
        plt.xlim(min(dates) - datetime.timedelta(days=7),
                 dates[0] + datetime.timedelta(days=3))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))

    plt.title('Healthcare Worker Burnout Trajectory Analysis',
              fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Burnout Score (0-100)', fontsize=10)
    plt.ylim(0, 105)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left', frameon=True)

    plt.xticks(rotation=25)
    plt.tight_layout()

    # Save the chart as an image in a folder(Burnout folder)
    image_filename = "burnout_trend.png"
    plt.savefig(image_filename, dpi=300)
    plt.close()  # This should close the plot figure to free memory

    print(
        f"Chart successfully saved as '{image_filename}' in your workspace directory.")


def main_menu():
    """Start up startup menu to direct user workflow."""
    while True:
        print("=" * 60)
        print("     HEALTHCARE WORKER BURNOUT MANAGEMENT SYSTEM      ")
        print("=" * 60)
        print("1. Log New Weekly Assessment & Generate Trend Chart")
        print("2. View/Filter Existing Trajectory Chart")
        print("3. Exit Application")
        print('-' * 60)
        choice = input("Enter your selection (1-3): ").strip()

        if choice == "1":
            run_tracker()
        elif choice == "2":
            plot_burnout_history()
        elif choice == "3":
            print("\nExiting application. Stay balanced and take care!")
        else:
            print("\nInvalid choice. Please select 1, 2, or 3. \n")


if __name__ == "__main__":
    main_menu()
