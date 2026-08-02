# Applied AI System: The Impossible Guesser + AI Coach

**Base project:** This extends *Game Glitch Investigator: The Impossible Guesser* (AI110 Module 1,
see [original repo](https://github.com/ZaydulHasan/ai110-module1show-gameglitchinvestigator-starter)),
a Streamlit number-guessing game. The original project's goal was to find and fix four AI-generated
bugs: backwards High/Low hints, a secret number that reset on every interaction, a Hard mode that was
easier than Normal mode, and a logic file full of placeholder crashes. All four bugs were fixed and
verified with automated pytest tests.

## What's New in This Version
This version adds an **agentic AI Coach** (`coach.py`) that analyzes the player's guess history after
every guess, proposes a statistically optimal next guess, scores its own confidence in that
suggestion, and decides whether to share advice or explicitly defer to the player when the stakes
are high and it isn't confident enough. This satisfies the required "Agentic Workflow" AI feature:
the coach doesn't just retrieve information, it analyzes state, proposes an action, evaluates its
own confidence, and decides whether to act or defer -- the same act-or-defer pattern used by
higher-stakes autonomous systems.

## Architecture
See `diagrams/architecture.mmd` for the full flow. In short: the Coach Agent sits between the game's
session state and the UI. After each guess it analyzes the remaining number range (narrowing it based
on "Too High"/"Too Low" outcomes), proposes a midpoint guess and hint text (via an LLM call if
`OPENAI_API_KEY` is set, otherwise a deterministic fallback template so the app is always
reproducible offline), computes a confidence score, and either surfaces the tip in an expander or
explicitly tells the player it is deferring. Every coach decision is logged to
`st.session_state.coach_log` for later inspection.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. (Optional) Enable LLM-generated hints: `export OPENAI_API_KEY=your_key`
3. Run the app: `python -m streamlit run app.py`
4. Run the unit tests: `pytest tests/`
5. Run the reliability harness: `python tests/test_harness.py`

## Sample Interactions
```
Attempt 1: Guessed 50 -> Go HIGHER!
Attempt 2: Guessed 70 -> Go HIGHER!

AI Coach: "Try narrowing toward the middle of the remaining range - around 85 is statistically your best bet."
Action: act | Confidence: 0.79
```

## Design Decisions
- The coach defaults to a deterministic hint template (no API key required) so the whole system
  is reproducible in any environment, including automated grading, without relying on network access.
- Guardrail: the coach always defers when only one attempt remains and its confidence is below
  0.75, rather than risk giving confidently-wrong advice at the highest-stakes moment of the game.
- Confidence is a transparent, hand-tunable weighted heuristic (range narrowness + attempts
  remaining) rather than a black-box score, so its behavior can be unit tested directly.

## Testing Summary
```
============================= test session starts ==============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
collected 18 items

tests\test_coach.py ......                                              [ 33%]
tests\test_game_logic.py ............                                   [100%]

============================== 18 passed in 0.05s ===============================
test_harness.py results:
Simulated games: 20
Wins: 20/20
Average attempts used: 6.10
```

18 out of 18 tests passed. Across 20 simulated games the coach helped win 20/20 (100%) with an average of 6.10 attempts used.

## Reflection
Building the AI Coach clarified for me what "agentic" actually means in practice: it's not just calling an LLM, it's the analyze -> propose -> evaluate -> act-or-defer loop that makes the system accountable for its own confidence rather than always outputting an answer. Adding the guardrail (deferring when confidence is low and attempts are critical) was the part that taught me the most -- without it, the coach behaved impressively most of the time but could fail silently at the exact moment its advice mattered most. Writing unit tests for coach.py and the 20-game reliability harness also forced me to think about edge cases I hadn't considered while just playing the game manually, like what happens when the guessable range narrows to a single number.
