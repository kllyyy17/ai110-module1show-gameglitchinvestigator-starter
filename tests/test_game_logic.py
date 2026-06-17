from logic_utils import check_guess, update_score


# ---------------------------------------------------------------------------
# Sanity: check_guess returns a (outcome, message) tuple, not a bare string.
# ---------------------------------------------------------------------------
def test_returns_outcome_and_message_tuple():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert isinstance(message, str)


# ---------------------------------------------------------------------------
# Bug #1 (FIXED): the high/low hint direction was inverted.
#
# "Too High" must point the player LOWER and "Too Low" must point HIGHER.
# ---------------------------------------------------------------------------
def test_too_high_outcome():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_too_low_outcome():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_tells_player_to_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_too_low_tells_player_to_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message.upper()
    assert "LOWER" not in message.upper()


def test_reported_glitch_scenario():
    # The exact case the player reported: secret 62, guess 50.
    # 50 < 62, so the hint must send them HIGHER.
    outcome, message = check_guess(50, 62)
    assert outcome == "Too Low"
    assert "HIGHER" in message.upper()


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# ---------------------------------------------------------------------------
# Bug #2 (FIXED): string secret used to trigger lexicographic comparison.
#
# check_guess now compares numerically, so a string secret behaves exactly
# like the equivalent integer secret.
# ---------------------------------------------------------------------------
def test_string_secret_single_digit_guess_is_too_low():
    # 9 < 62 numerically -> "Too Low" (used to wrongly be "Too High").
    outcome, _ = check_guess(9, "62")
    assert outcome == "Too Low"


def test_string_secret_large_guess_is_too_high():
    # 100 > 62 numerically -> "Too High" (used to wrongly be "Too Low").
    outcome, _ = check_guess(100, "62")
    assert outcome == "Too High"


def test_string_secret_matches_numeric_secret():
    # Comparing against "62" must behave identically to comparing against 62.
    assert check_guess(50, "62") == check_guess(50, 62)
    assert check_guess(9, "62") == check_guess(9, 62)


# ---------------------------------------------------------------------------
# Bug #3 (FIXED): update_score secretly ADDED points for a wrong "Too High"
# guess on even attempts, and the win bonus had an off-by-one.
# ---------------------------------------------------------------------------
def test_wrong_guess_always_loses_points():
    # A wrong guess must cost 5 points no matter the attempt parity.
    assert update_score(100, "Too High", 1) == 95
    assert update_score(100, "Too High", 2) == 95  # used to be 105 (the bug)
    assert update_score(100, "Too Low", 2) == 95


def test_win_bonus_rewards_fewer_attempts():
    # Winning on attempt 1 should score higher than winning on a later attempt.
    assert update_score(0, "Win", 1) == 90
    assert update_score(0, "Win", 1) > update_score(0, "Win", 5)
