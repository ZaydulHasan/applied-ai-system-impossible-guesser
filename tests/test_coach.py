from coach import analyze_state, compute_confidence, decide_action, coach_suggest


def test_analyze_state_narrows_range_on_too_high():
    history = [{"guess": 80, "outcome": "Too High"}]
    state = analyze_state(1, 100, history)
    assert state["high"] == 79

def test_analyze_state_narrows_range_on_too_low():
    history = [{"guess": 20, "outcome": "Too Low"}]
    state = analyze_state(1, 100, history)
    assert state["low"] == 21

def test_confidence_increases_as_range_shrinks():
    wide = compute_confidence(range_size=90, attempts_left=5, full_range=100)
    narrow = compute_confidence(range_size=5, attempts_left=5, full_range=100)
    assert narrow > wide

def test_decide_action_defers_on_low_confidence_and_low_attempts():
    assert decide_action(confidence=0.4, attempts_left=1) == "defer"

def test_decide_action_acts_on_high_confidence():
    assert decide_action(confidence=0.9, attempts_left=3) == "act"

def test_coach_suggest_returns_expected_keys():
    result = coach_suggest(1, 100, [], attempts_left=8, full_range=100)
    assert set(result.keys()) == {"action", "confidence", "suggested_midpoint", "message"}
