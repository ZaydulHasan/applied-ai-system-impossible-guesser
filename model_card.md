# Model Card: AI Coach (Impossible Guesser)

This document is the graded responsible-AI reflection for the AI Coach feature added on top of
the Module 1 Impossible Guesser game. Please answer each section honestly and specifically --
this is meant to capture real testing observations and real AI-collaboration moments, not
generic statements.

## Limitations & Biases
- The confidence heuristic in `compute_confidence()` is a simple hand-weighted formula (range
  narrowness + attempts-remaining buffer), not a calibrated statistical model. It can be
  overconfident or underconfident, especially early in a game when little history exists.
- When `OPENAI_API_KEY` is set, hint text becomes non-deterministic and its exact wording is not
  unit-tested beyond checking that a string is returned -- the LLM could occasionally produce a
  misleading or overly specific hint despite the prompt constraints.
- The coach only reasons about the numeric search space; it has no awareness of a player's actual
  strategy or intent, so its advice can feel repetitive across games.

PASTE YOUR OWN NOTES HERE: add anything else you noticed about limitations/biases while testing.

## Potential Misuse
- If the guardrail thresholds in `decide_action()` were removed or lowered, the coach could be
  made to always reveal a near-exact answer, defeating the purpose of the guessing game.
  This is mitigated by hard-coding the defer-on-low-confidence/low-attempts rule directly in the
  decision function rather than making it a configurable/overridable parameter exposed to the UI.
- A malicious modification could swap the fallback template for misleading text; since the
  fallback path has no external verification, code review is the main safeguard.

## What Surprised Me While Testing
PASTE YOUR OWN NOTES HERE: for example, did the coach defer more or less often than you expected?
Did the confidence scores line up with your own intuition about how close a guess was? Did the
harness's simulated win rate surprise you?

## AI Collaboration
Describe your collaboration with an AI assistant while building this feature.

- **Helpful suggestion:** PASTE YOUR OWN NOTES HERE -- describe one specific instance where the
  AI (e.g. this coach design, or an AI coding assistant you used) gave you a suggestion that
  genuinely improved the project.
- **Flawed suggestion:** PASTE YOUR OWN NOTES HERE -- describe one specific instance where you had
  to correct, reject, or rework something the AI suggested, and explain why it was wrong or
  insufficient.
