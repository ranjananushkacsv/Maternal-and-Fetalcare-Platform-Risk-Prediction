import streamlit as st
import time

# Function to format time in MM:SS format
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def run_meditation():
    st.title("Pregnancy Meditation Guide")

    # List of meditation exercises
    exercises = [
        "🌿 Deep Belly Breathing",
        "🌊 Ocean Wave Visualization",
        "🕯️ Candle Flame Focus",
        "🌞 Morning Sun Meditation",
        "💖 Loving-Kindness Meditation",
        "🌙 Moonlight Relaxation",
        "🌲 Forest Walk Visualization",
        "🎵 Soft Humming Meditation",
    ]

    st.write("Take a deep breath and begin your relaxation journey. Each meditation lasts **2 minutes**, followed by a **20-second break**.")

    # Initialize session state variables
    if "started" not in st.session_state:
        st.session_state.started = False
    if "current_exercise" not in st.session_state:
        st.session_state.current_exercise = 0
    if "paused" not in st.session_state:
        st.session_state.paused = False
    if "time_left" not in st.session_state:
        st.session_state.time_left = 120

    # Start Meditation Button
    if not st.session_state.started:
        if st.button("▶️ Start Meditation"):
            st.session_state.started = True
            st.rerun()

    # If meditation has started, display exercises
    if st.session_state.started:
        if st.session_state.current_exercise < len(exercises):
            exercise = exercises[st.session_state.current_exercise]
            st.subheader(f"🧘 Exercise {st.session_state.current_exercise + 1}: {exercise}")

            # Timer Display with Centered Big Font
            timer_placeholder = st.empty()

            # Pause/Resume Button
            if st.button(" Pause" if not st.session_state.paused else " Resume", key="pause_btn"):
                st.session_state.paused = not st.session_state.paused

            # Timer Logic
            if not st.session_state.paused:
                if st.session_state.time_left > 0:
                    timer_placeholder.markdown(
                        f"""
                        <div style="text-align:center; font-size:50px; font-weight:bold; color:#FF4500;">
                            ⏳ {format_time(st.session_state.time_left)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    time.sleep(1)
                    st.session_state.time_left -= 1
                    st.rerun()
                else:
                    st.success("✅ Exercise complete! Time for a short break.")
                    st.session_state.time_left = 20  # Reset timer for break
                    st.session_state.current_exercise += 1
                    st.rerun()
            else:
                timer_placeholder.markdown(
                    f"""
                    <div style="text-align:center; font-size:50px; font-weight:bold; color:#888;">
                        ⏸️ Paused at {format_time(st.session_state.time_left)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:
            st.success("🎉 Meditation session complete! You did amazing! 🙌")
            st.session_state.started = False  # Reset for next session

# Run the meditation function
if __name__ == "__main__":
    run_meditation()
