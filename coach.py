"""
coach.py - Agentic AI Coach for the Impossible Guesser game.

Implements an analyze -> propose -> evaluate -> act/defer workflow:
1. ANALYZE current guess history and remaining range
2. PROPOSE an optimal next guess + natural-language hint
3. EVALUATE confidence in that suggestion
4. DECIDE whether to act (show the tip) or defer (let the player proceed alone)
"""

import os


def analyze_state(low: int, high: int, history: list) -> dict:
    """Look at guess history and compute the remaining search space."""
    for entry in history:
        if entry["outcome"] == "Too High":
            high = min(high, entry["guess"] - 1)
        elif entry["outcome"] == "Too Low":
            low = max(low, entry["guess"] + 1)

    midpoint = (low + high) // 2
    range_size = max(high - low, 1)
    return {"low": low, "high": high, "midpoint": midpoint, "range_size": range_size}


def compute_confidence(range_size: int, attempts_left: int, full_range: int) -> float:
    """
    Confidence heuristic: higher when the remaining search space is small
    relative to the attempts left. Returns a 0.0-1.0 score.
    """
    if attempts_left <= 0:
        return 0.0
    narrowness = 1 - (range_size / max(full_range, 1))
    attempt_buffer = min(attempts_left / 3, 1.0)
    confidence = round((0.7 * narrowness + 0.3 * attempt_buffer), 2)
    return max(0.0, min(confidence, 1.0))


def generate_hint_text(midpoint: int, confidence: float) -> str:
    """
    Produce a natural-language hint. Uses an LLM if OPENAI_API_KEY is set,
    otherwise falls back to a deterministic template so the app always
    runs reproducibly offline.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                f"You are a coach for a number-guessing game. The optimal next "
                f"guess is {midpoint}. Confidence in this suggestion is {confidence}. "
                f"Give one short, encouraging sentence of advice without stating the "
                f"exact number outright."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=40,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Guardrail: never let an API failure crash the game
            return f"(AI hint unavailable, using fallback) Try something near the middle of the remaining range. [{e}]"

    # Deterministic fallback (no API key / offline mode)
    return f"Try narrowing toward the middle of the remaining range - around {midpoint} is statistically your best bet."


def decide_action(confidence: float, attempts_left: int, threshold: float = 0.55) -> str:
    """
    Guardrail decision: act (show hint) if confident enough, otherwise defer.
    Always defer when attempts are critically low and confidence isn't high,
    to avoid the AI giving misleadingly authoritative advice under high stakes.
    """
    if attempts_left <= 1 and confidence < 0.75:
        return "defer"
    if confidence >= threshold:
        return "act"
    return "defer"


def coach_suggest(low: int, high: int, history: list, attempts_left: int, full_range: int) -> dict:
    """Main orchestration: analyze -> propose -> evaluate -> decide."""
    state = analyze_state(low, high, history)
    confidence = compute_confidence(state["range_size"], attempts_left, full_range)
    action = decide_action(confidence, attempts_left)

    if action == "act":
        message = generate_hint_text(state["midpoint"], confidence)
    else:
        message = (
            "I'm not confident enough to help with this one - "
            "the stakes are high and my suggestion could be wrong. You're on your own for this guess!"
        )

    return {
        "action": action,
        "confidence": confidence,
        "suggested_midpoint": state["midpoint"],
        "message": message,
    }
