"""Friendly self-check helpers for exercises.

Checks report a helpful hint rather than exposing a hidden solution.
"""

from __future__ import annotations


def check(condition: bool, hint: str = "Review the previous step and try again.") -> bool:
    """Print friendly feedback and return whether the learner passed."""
    if bool(condition):
        print("✓ Check passed. Nicely done!")
        return True
    print(f"Not quite yet. Hint: {hint}")
    return False


def equal(actual: object, expected: object, hint: str) -> bool:
    """Check exact equality for simple exercises."""
    return check(actual == expected, hint)
