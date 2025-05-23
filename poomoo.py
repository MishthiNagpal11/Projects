# pomo.py
import streamlit as st
import time
import base64
from datetime import datetime
import random

# Helper to encode background image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("beach.jpg")
st.set_page_config(page_title="Focus With Me", layout="wide")

# Styling
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    padding-top: 2rem;
    overflow-x: hidden;
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

.timer-text {{
    font-size: 100px;
    font-weight: 600;
    color: white;
    text-align: center;
    margin-bottom: 40px;
}}
</style>
""", unsafe_allow_html=True)

# Styling for the focus heading and search bar
st.markdown("""
<style>
    .focus-header {
        text-align: center;
        font-weight: bold;
        color: white;
        font-size: 50px;
        margin-top: 0px;  /* Less space from the top */
        margin-bottom: 2px;  /* Space below the heading */
    }

    .stTextInput>div>div>input {
        margin-top: -5px;  /* Reducing space between the search bar and the heading */
    }
</style>
""", unsafe_allow_html=True)

# Focus header
st.markdown('<h1 class="focus-header">Focus With Me</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: white;">Stay focused and productive!</h2>', unsafe_allow_html=True)

# Audio player for soothing song
st.markdown("""
    <style>
    .audio-player {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
if "start" not in st.session_state:
    st.session_state.start = time.time()

elapsed = time.time() - st.session_state.start
if elapsed > 150:
    st.session_state.start = time.time()
    st.experimental_rerun()


# Use st.audio to embed the audio file
st.audio("hearty.mp3", format="audio/mp3", start_time=0)

# Session state
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
if "pin" not in st.session_state:
    st.session_state.pin = str(random.randint(1000, 9999))
if "selected_game" not in st.session_state:
    st.session_state.selected_game = None
if "math_problem" not in st.session_state:
    st.session_state.math_problem = (random.randint(1, 20), random.randint(1, 20))
if "guess_target" not in st.session_state:
    st.session_state.guess_target = random.randint(1, 5)
if "rps_bot_move" not in st.session_state:
    st.session_state.rps_bot_move = random.choice(["Rock", "Paper", "Scissors"])
if "scramble_word" not in st.session_state:
    st.session_state.scramble_word = random.choice(["focus", "energy", "streamlit", "python", "timer", "coding"])
if "scrambled_version" not in st.session_state:
    word = st.session_state.scramble_word
    st.session_state.scrambled_version = ''.join(random.sample(word, len(word)))

# Columns layout
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown(f'<div class="focus-room">Focus Room PIN: {st.session_state.pin}</div>', unsafe_allow_html=True)
    option = st.radio("Create or Join Session:", ["Create Session", "Join Session"])
    if option == "Create Session":
        st.write(f"Your session PIN is {st.session_state.pin}")
        st.write("Share this PIN with others to join your session.")
    elif option == "Join Session":
        pin_input = st.text_input("Enter Session PIN")
        if st.button("Join"):
            if pin_input == st.session_state.pin:
                st.success("You have joined the Focus Room!")
            else:
                st.error("Invalid PIN! Please try again.")

# Timer modes
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

# Timer logic
now = datetime.now()
if st.session_state.is_running:
    if st.session_state.start_time is None:
        st.session_state.start_time = now
    elapsed = (now - st.session_state.start_time).total_seconds()
    time_left = max(0, st.session_state.duration - int(elapsed))
    st.session_state.paused_time_left = time_left
else:
    time_left = st.session_state.paused_time_left

mins, secs = divmod(time_left, 60)
st.markdown(f'<div class="timer-text">{int(mins):02d}:{int(secs):02d}</div>', unsafe_allow_html=True)

# Timer control
left_spacer, col1, col2, col3, right_spacer = st.columns([2, 2, 1, 2, 2])
with col1:
    if st.button("▶ Start" if not st.session_state.is_running else "‖ Pause"):
        st.session_state.is_running = not st.session_state.is_running
        if st.session_state.is_running:
            st.session_state.start_time = datetime.now()

with col3:
    if st.button("🔄 Reset"):
        st.session_state.duration = durations[st.session_state.mode]
        st.session_state.paused_time_left = durations[st.session_state.mode]
        st.session_state.is_running = False
        st.session_state.start_time = None
        st.session_state.selected_game = None
        st.session_state.math_problem = (random.randint(1, 20), random.randint(1, 20))
        st.session_state.guess_target = random.randint(1, 5)
        st.session_state.rps_bot_move = random.choice(["Rock", "Paper", "Scissors"])
        st.session_state.scramble_word = random.choice(["focus", "energy", "streamlit", "python", "timer", "coding"])
        st.session_state.scrambled_version = ''.join(random.sample(st.session_state.scramble_word, len(st.session_state.scramble_word)))
        st.rerun()
if "time_bank" not in st.session_state:
    st.session_state.time_bank = 0  # Initialize time bank

# Display accumulated time bank
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(f'<div class="focus-room">Focus Room PIN: {st.session_state.pin}</div>', unsafe_allow_html=True)

# Timer logic for session start or pause
if st.session_state.is_running:
    if st.session_state.start_time is None:
        st.session_state.start_time = now
    elapsed = (now - st.session_state.start_time).total_seconds()
    time_left = max(0, st.session_state.duration - int(elapsed))
    st.session_state.paused_time_left = time_left
else:
    time_left = st.session_state.paused_time_left

# Check if the time left reaches zero and apply the time bank
if time_left <= 0 and st.session_state.time_bank > 0:
    st.session_state.time_bank -= 30  # Subtract the time used from the bank
    st.session_state.paused_time_left += 30  # Add it to the current session
    st.experimental_rerun()  # Refresh the timer after applying the bank


# Display accumulated time bank
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(f'<div class="focus-room">Focus Room PIN: {st.session_state.pin}</div>', unsafe_allow_html=True)
    st.write(f"Time Bank: {st.session_state.time_bank // 60}m {st.session_state.time_bank % 60}s")


# Mini-games logic (only during Short Break)
def show_mini_games():
    st.markdown("<hr style='margin:1rem 0;border:1px solid white;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white;text-align:center;'>🎮 Short Break Games</h3>", unsafe_allow_html=True)

    game_cols = st.columns([1, 1, 1, 1])
    if st.session_state.selected_game is None:
        with game_cols[0]:
            if st.button("🧠 Math"):
                st.session_state.selected_game = "math"
        with game_cols[1]:
            if st.button("🎯 Guess"):
                st.session_state.selected_game = "guess"
        with game_cols[2]:
            if st.button("🪨✂️📄 RPS"):
                st.session_state.selected_game = "rps"
        with game_cols[3]:
            if st.button("🔠 Scramble"):
                st.session_state.selected_game = "scramble"

    with st.container():
        if st.session_state.selected_game == "math":
            a, b = st.session_state.math_problem
            answer = st.text_input(f"What is {a} + {b}?", key="math_input")
            if st.button("Submit Math Answer"):
                if answer == str(a + b):
                    st.success("Correct! +30 seconds to Time Bank!")
                    st.session_state.time_bank += 30  # Add to the time bank
                    st.session_state.selected_game = None
                    st.session_state.math_problem = (random.randint(1, 20), random.randint(1, 20))
                else:
                    st.error("Wrong!")

        elif st.session_state.selected_game == "guess":
            guess = st.number_input("Guess 1-5:", min_value=1, max_value=5, step=1, key="guess_input")
            if st.button("Submit Guess"):
                correct = st.session_state.guess_target
                if guess == correct:
                    st.success("Lucky hit! +30 seconds to Time Bank!")
                    st.session_state.time_bank += 30  # Add to the time bank
                else:
                    st.warning(f"Nope! It was {correct}.")
                st.session_state.selected_game = None
                st.session_state.guess_target = random.randint(1, 5)

        elif st.session_state.selected_game == "rps":
            move = st.selectbox("Choose:", ["Rock", "Paper", "Scissors"], key="rps_input")
            if st.button("Play RPS"):
                bot = st.session_state.rps_bot_move
                result = "Draw"
                if (move == "Rock" and bot == "Scissors") or \
                   (move == "Scissors" and bot == "Paper") or \
                   (move == "Paper" and bot == "Rock"):
                    result = "Win"
                    st.session_state.time_bank += 30  # Add to the time bank
                elif move != bot:
                    result = "Lose"

                st.markdown(f"<div style='color:white;font-size:20px;text-align:center;'>You: {move} &nbsp;&nbsp;&nbsp; Bot: {bot} &nbsp;&nbsp;&nbsp; → <b>{result}</b></div>", unsafe_allow_html=True)
                st.session_state.selected_game = None
                st.session_state.rps_bot_move = random.choice(["Rock", "Paper", "Scissors"])

        elif st.session_state.selected_game == "scramble":
            word = st.session_state.scramble_word
            scrambled = st.session_state.scrambled_version
            user_input = st.text_input(f"Unscramble this: {scrambled}", key="scramble_input")
            if st.button("Check Word"):
                if user_input.lower() == word:
                    st.success("Correct! +30 seconds to Time Bank")
                    st.session_state.time_bank += 30  # Add to the time bank
                    new_word = random.choice(["focus", "energy", "streamlit", "python", "timer", "coding"])
                    while new_word == word:
                        new_word = random.choice(["focus", "energy", "streamlit", "python", "timer", "coding"])
                    st.session_state.scramble_word = new_word
                    st.session_state.scrambled_version = ''.join(random.sample(new_word, len(new_word)))
                    st.session_state.selected_game = None
                else:
                    st.error("Try again!")


if st.session_state.mode == "Short Break" and st.session_state.is_running:
    show_mini_games()

# Auto rerun if running
if st.session_state.is_running and time_left > 0:
    time.sleep(1)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()
