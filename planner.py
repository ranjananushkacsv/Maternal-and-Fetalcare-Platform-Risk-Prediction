import streamlit as st
import datetime
import random

def run_planner():
    st.title("🤰 Pregnancy Planner")

    # List of Pregnancy-Related Thoughts
    thoughts = [
        "🌸 Every kick is a reminder that a miracle is growing inside you.",
        "🤰 Your body is creating life—embrace the beauty of the journey!",
        "💖 You are braver than you believe, stronger than you seem, and loved more than you know.",
        "🌿 The littlest feet make the biggest footprints in our hearts.",
        "🍼 Every day brings you closer to the most precious moment of your life.",
        "🌟 You are not just growing a baby, but also a mother. Be proud of yourself!",
        "✨ Trust your body, trust your journey, and trust the beautiful process of motherhood.",
    ]

    # Select a Random Thought on Refresh
    thought_of_the_day = random.choice(thoughts)
    
    # Display Thought of the Day
    st.subheader("💭 Today's Thought of the Day")
    st.write(f"**{thought_of_the_day}**")

    # Initialize session state
    if "trimester" not in st.session_state:
        st.session_state["trimester"] = "First Trimester"
    if "due_date" not in st.session_state:
        st.session_state["due_date"] = None
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = {
            "First Trimester": [
                "Book first prenatal appointment",
                "Start taking prenatal vitamins",
                "Maintain a healthy diet",
            ],
            "Second Trimester": [
                "Plan a gender reveal (if desired)",
                "Look into birthing classes",
                "Buy maternity clothes",
            ],
            "Third Trimester": [
                "Pack hospital bag",
                "Set up the nursery",
                "Discuss birth plan with doctor",
            ],
        }

    # Select Trimester
    trimester = st.selectbox("Select your trimester:", ["First Trimester", "Second Trimester", "Third Trimester"])
    st.session_state["trimester"] = trimester

    # Due Date Input
    due_date = st.date_input("Enter your due date:", value=datetime.date.today() + datetime.timedelta(days=280))
    st.session_state["due_date"] = due_date

    # Pregnancy Progress Calculation
    today = datetime.date.today()
    conception_date = due_date - datetime.timedelta(days=280)  # Approximate conception date
    weeks_pregnant = (today - conception_date).days // 7

    # Ensure progress is within the valid range [0.0, 1.0]
    progress = max(0.0, min(weeks_pregnant / 40, 1.0))
    st.progress(progress)

    # Task List (Tasks Disappear When Checked)
    st.subheader(f"📝 {trimester} Checklist")

    # Display tasks dynamically
    tasks = st.session_state["tasks"][trimester]
    updated_tasks = []

    for i, task in enumerate(tasks):
        key = f"{trimester}_{task}"  # Unique key for checkboxes
        if not st.checkbox(task, key=key):  # If not checked, keep it
            updated_tasks.append(task)

    # Update the session state with remaining tasks
    if len(updated_tasks) < len(tasks):  # Only update if at least one task was checked
        st.session_state["tasks"][trimester] = updated_tasks

    # Add New Task
    new_task = st.text_input("Add a new task:", placeholder="E.g., Schedule ultrasound, Buy baby clothes")
    if st.button("Add Task"):
        if new_task:
            st.session_state["tasks"][trimester].append(new_task)
            st.rerun()

# Run the planner function when script is executed
if __name__ == "__main__":
    run_planner()
