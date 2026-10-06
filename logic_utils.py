#FIX: Refactored logic into logic_utils.py using agent mode
# (ranges now widen with difficulty: Easy < Normal < Hard)
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


#FIX: Refactored logic into logic_utils.py using agent mode
# (attempt limits moved out of app.py; harder = fewer attempts)
def get_attempt_limit(difficulty: str):
    """Return the number of guesses allowed. Harder means fewer guesses for a wider range."""
    if difficulty == "Easy":
        return 10
    if difficulty == "Normal":
        return 8
    if difficulty == "Hard":
        return 6
    return 8


#FIX: Refactored logic into logic_utils.py using agent mode
# (whole numbers only, range check, no str/float mix-ups)
def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess. Only whole numbers are accepted,
    since the secret is always an int. If low/high are given, the guess
    must also fall inside that inclusive range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number (e.g. 42)."

    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


#FIX: Refactored logic into logic_utils.py using agent mode
# (hints no longer backwards, no str comparison fallback, int-only check)
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if not isinstance(guess, int) or not isinstance(secret, int):
        raise TypeError(
            f"guess and secret must both be int, got "
            f"{type(guess).__name__} and {type(secret).__name__}"
        )

    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


#FIX: Refactored logic into logic_utils.py using agent mode
# (moved from app.py, scoring rules unchanged)
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
