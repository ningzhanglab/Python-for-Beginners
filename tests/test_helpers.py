"""Friendly checks must not expose solutions or raise on a wrong answer."""

from pss_helpers.checks import check, equal


def test_check_feedback(capsys):
    assert check(True)
    assert not check(False, "Review the row count")
    captured = capsys.readouterr().out
    assert "Check passed" in captured
    assert "Review the row count" in captured
    assert "AssertionError" not in captured


def test_equal_feedback():
    assert equal(4, 4, "Recompute")
    assert not equal(3, 4, "Recompute")
