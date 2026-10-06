import pytest

from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_rejects_string_secret():
    # The secret must stay an int; a str secret should fail loudly
    with pytest.raises(TypeError):
        check_guess(50, "50")

def test_parse_guess_accepts_whole_number():
    assert parse_guess(" 42 ") == (True, 42, None)

def test_parse_guess_rejects_non_integers():
    for raw in ["", "abc", "4.5", "4.0"]:
        ok, value, err = parse_guess(raw)
        assert not ok and value is None and err

def test_parse_guess_rejects_out_of_range():
    for raw in ["0", "-3", "101", "500"]:
        ok, value, err = parse_guess(raw, 1, 100)
        assert not ok and value is None and "between 1 and 100" in err

def test_parse_guess_accepts_range_edges():
    assert parse_guess("1", 1, 100) == (True, 1, None)
    assert parse_guess("100", 1, 100) == (True, 100, None)

def test_harder_difficulty_has_wider_range_and_fewer_attempts():
    levels = ["Easy", "Normal", "Hard"]
    ranges = [get_range_for_difficulty(d)[1] for d in levels]
    limits = [get_attempt_limit(d) for d in levels]
    assert ranges == sorted(ranges) and len(set(ranges)) == 3
    assert limits == sorted(limits, reverse=True) and len(set(limits)) == 3

# --- Regression tests for the "hints were backwards" bug ---

def test_too_high_guess_says_go_lower():
    # Bug: a guess above the secret used to say "Go HIGHER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_guess_says_go_higher():
    # Bug: a guess below the secret used to say "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_numeric_not_alphabetical_comparison():
    # Bug: on even attempts the secret was turned into a str, so "9" > "50"
    # alphabetically and 9 was wrongly called "Too High" against a secret of 50.
    outcome, message = check_guess(9, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_hints_consistent_for_every_attempt_parity():
    # Bug: hints differed between odd and even attempts. The same guess and
    # secret must always give the same answer, whatever the attempt number.
    results = {check_guess(30, 75) for _ in range(4)}
    assert results == {("Too Low", "📈 Go HIGHER!")}
