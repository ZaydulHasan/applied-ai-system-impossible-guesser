from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# --- check_guess tests ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # FIX: guess=60 is higher than secret=50, hint must say LOWER not HIGHER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # FIX: guess=40 is lower than secret=50, hint must say HIGHER not LOWER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok == False
    assert err == "Enter a guess."

def test_parse_non_number():
    ok, value, err = parse_guess("hello")
    assert ok == False

def test_parse_decimal():
    ok, value, err = parse_guess("42.0")
    assert ok == True
    assert value == 42

# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_range_is_harder_than_normal():
    # FIX: Hard mode must have a bigger range than Normal (1-100)
    low, high = get_range_for_difficulty("Hard")
    assert high > 100

# --- update_score tests ---

def test_win_increases_score():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_too_low_decreases_score():
    new_score = update_score(50, "Too Low", 1)
    assert new_score < 50
