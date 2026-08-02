"""
Simulates several complete games using the AI coach and prints a
pass/fail reliability summary. Run with: python tests/test_harness.py
"""
import os
import sys
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic_utils import get_range_for_difficulty, check_guess
from coach import coach_suggest


def simulate_game(difficulty="Normal", attempt_limit=8, seed=None):
    if seed is not None:
        random.seed(seed)
    low, high = get_range_for_difficulty(difficulty)
    secret = random.randint(low, high)
    history = []
    for attempt in range(1, attempt_limit + 1):
        attempts_left = attempt_limit - attempt + 1
        result = coach_suggest(low, high, history, attempts_left, high - low)
        guess = result["suggested_midpoint"]
        outcome, _ = check_guess(guess, secret)
        history.append({"guess": guess, "outcome": outcome})
        if outcome == "Win":
            return {"won": True, "attempts_used": attempt, "coach_log": history}
    return {"won": False, "attempts_used": attempt_limit, "coach_log": history}


if __name__ == "__main__":
    results = [simulate_game(seed=i) for i in range(20)]
    wins = sum(r["won"] for r in results)
    avg_attempts = sum(r["attempts_used"] for r in results) / len(results)
    print(f"Simulated games: {len(results)}")
    print(f"Wins: {wins}/{len(results)}")
    print(f"Average attempts used: {avg_attempts:.2f}")
