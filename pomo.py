import streamlit as st
import time
import base64
from datetime import datetime
import random

# Load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("beach.jpg")

# Page Config
st.set_page_config(page_title="Focus With Me", layout="wide")

# CSS Styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bg_image}"); 
        background-size: cover; 
        background-position: center;
        background-attachment: fixed;
        padding-top: 2rem;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"], footer {{
        visibility: hidden;
    }}
    .focus-room {{
        position: fixed;
        left: 10px;
        top: 50px;
        width: 250px;
        height: auto;
        color: white;
        font-size: 18px;
        text-align: left;
        background: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 10px;
        z-index: 1000;
    }}
    .timer-container {{
        width: 100%;
        text-align: center;
        margin-top: 20px;
    }}
    .timer-text {{
        font-size: 100px;
        font-weight: 600;
        color: white;
        text-align: center;
        margin-bottom: 40px;
    }}
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "mode" not in st.session_state:
    st.session_state.mode = "Pomodoro"
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "duration" not in st.session_state:
    st.session_state.duration = 25 * 60
if "paused_time_left" not in st.session_state:
    st.session_state.paused_time_left = 25 * 60

# Focus Room - PIN System
if "pin" not in st.session_state:
    st.session_state.pin = str(random.randint(1000, 9999))

# Layout using Streamlit columns
col1, col2 = st.columns([1, 3])  # Left small for Focus Room, right large for Timer

with col1:
    # Fixed Focus Room Panel
    st.markdown(f'<div class="focus-room">Focus Room PIN: {st.session_state.pin}</div>', unsafe_allow_html=True)
    option = st.radio("Create or Join Session", ["Create Session", "Join Session"])
    if option == "Create Session":
        st.write(f"Your session PIN: {st.session_state.pin}")
        st.write("Share this PIN with others to join your session.")
    elif option == "Join Session":
        pin_input = st.text_input("Enter Session PIN")
        if st.button("Join"):
            if pin_input == st.session_state.pin:
                st.success("You have joined the Focus Room!")
            else:
                st.error("Invalid PIN! Please try again.")

with col2:
    # Timer Section
    st.markdown("""
        <h1 style="text-align:center; font-weight:bold; color:white;">
            Focus With Me
        </h1>
    """, unsafe_allow_html=True)

    durations = {
        "Pomodoro": 25 * 60,
        "Short Break": 5 * 60,
        "Long Break": 15 * 60
    }

    left_spacer, col1, col2, col3, right_spacer = st.columns([1, 2, 2, 2, 1])
    with col1:
        if st.button("Pomodoro"):
            st.session_state.mode = "Pomodoro"
            st.session_state.duration = durations["Pomodoro"]

    with col2:
        if st.button("Short Break"):
            st.session_state.mode = "Short Break"
            st.session_state.duration = durations["Short Break"]

    with col3:
        if st.button("Long Break"):
            st.session_state.mode = "Long Break"
            st.session_state.duration = durations["Long Break"]

    # Timer Logic
    now = datetime.now()
    if st.session_state.is_running:
        if st.session_state.start_time is None:
            st.session_state.start_time = now
        elapsed = (now - st.session_state.start_time).total_seconds()
        time_left = max(0, st.session_state.duration - int(elapsed))
        st.session_state.paused_time_left = time_left
    else:
        time_left = st.session_state.paused_time_left

    # Display Timer
    mins, secs = divmod(time_left, 60)
    st.markdown(f"<div class='timer-text'>{int(mins):02d}:{int(secs):02d}</div>", unsafe_allow_html=True)

    # Start/Reset Buttons
    left_spacer, col1, col2, col3, right_spacer = st.columns([2, 2, 1, 2, 2])
    with col1:
        if st.button("⏵ Start" if not st.session_state.is_running else "⏸ Pause"):
            st.session_state.is_running = not st.session_state.is_running

    with col3:
        if st.button("🔁 Reset"):
            st.session_state.duration = durations[st.session_state.mode]
            st.session_state.paused_time_left = durations[st.session_state.mode]
            st.session_state.is_running = False
            st.session_state.start_time = None
            st.rerun()

    # Auto-refresh if running
    if st.session_state.is_running and time_left > 0:
        time.sleep(1)
        st.rerun()
