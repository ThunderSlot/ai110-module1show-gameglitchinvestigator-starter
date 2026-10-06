import random
import streamlit as st

#FIX: Refactored logic into logic_utils.py using agent mode
from logic_utils import (
    get_range_for_difficulty,
    get_attempt_limit,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

#FIX: Refactored logic into logic_utils.py using agent mode
# (attempt limit and range now come from logic_utils.py)
attempt_limit = get_attempt_limit(difficulty)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


#FIX: Refactored logic into logic_utils.py using agent mode
# (one reset helper: also resets status, history and score, uses the difficulty range)
def start_new_game():
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


#FIX: Refactored logic into logic_utils.py using agent mode
# First load, or the difficulty changed: the old secret may be outside the new range.
if st.session_state.get("difficulty") != difficulty:
    start_new_game()

st.subheader("Make a guess")

#FIX: Refactored logic into logic_utils.py using agent mode
# (attempts-left message and debug panel no longer lag one guess behind)
# Reserve the spots now, but fill them after the submit handler has updated state.
attempts_info = st.empty()
debug_panel = st.container()


def show_game_info():
    attempts_info.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_panel:
        with st.expander("Developer Debug Info"):
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: Refactored logic into logic_utils.py using agent mode
# (New Game now fully resets the game, so the status lock is cleared)
if new_game:
    start_new_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    show_game_info()
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    #FIX: Refactored logic into logic_utils.py using agent mode
    # (range check, no duplicate guesses, invalid input costs no attempt)
    # Invalid or repeated guesses don't cost an attempt and aren't recorded.
    if not ok:
        st.error(err)
    elif guess_int in st.session_state.history:
        st.warning(f"You already guessed {guess_int}. Try a different number.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        #FIX: Refactored logic into logic_utils.py using agent mode
        # (secret is always an int; the even/odd str(secret) hack is removed)
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

#FIX: Refactored logic into logic_utils.py using agent mode
# (drawn after the submit handler so the info is current)
show_game_info()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
