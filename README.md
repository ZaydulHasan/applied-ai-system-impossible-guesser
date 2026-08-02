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
PASTE REAL OUTPUT HERE: after playing a full game, copy 2-3 real guess/coach-response
pairs here (e.g. "Attempt 3: Guessed 62 -> Go LOWER! | AI Coach: Try narrowing toward ~31").
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
PASTE REAL "pytest tests/" OUTPUT HERE
PASTE REAL "python tests/test_harness.py" OUTPUT HERE
```

Add a short written summary too, for example: "X out of Y tests passed. Across 20 simulated
games the coach helped win Z% of the time with an average of N attempts used. The coach correctly
deferred instead of guessing wrong when attempts were critically low."

## Reflection
(Add your own reflection in your own words: what building the coach taught you about agentic
design, guardrails, and testing. The graded responsible-AI reflection -- your collaboration with
AI, one helpful and one flawed AI suggestion, and the system's limitations -- belongs in
`model_card.md`, not here.)
