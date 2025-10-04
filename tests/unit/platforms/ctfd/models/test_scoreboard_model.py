import pytest

from ctfbridge.models.scoreboard import ScoreboardEntry as CoreScoreboardEntry
from ctfbridge.platforms.ctfd.models.scoreboard import CTFdScoreboardEntry

sample_ctfd_scoreboard_entry_data = {
    "pos": 1,
    "account_id": 37,
    "account_url": "/play/users/37",
    "account_type": "user",
    "oauth_id": None,
    "name": "John",
    "score": 1337,
    "bracket_id": None,
    "bracket_name": None,
}


def test_ctfd_scoreboard_entry_parse():
    entry = CTFdScoreboardEntry(**sample_ctfd_scoreboard_entry_data)
    assert entry.pos == 1
    assert entry.name == "John"
    assert entry.score == 1337


def test_ctfd_scoreboard_entry_to_core_model():
    ctfd_entry = CTFdScoreboardEntry(**sample_ctfd_scoreboard_entry_data)
    core_entry = ctfd_entry.to_core_model()

    assert isinstance(core_entry, CoreScoreboardEntry)
    assert core_entry.rank == 1  # 'pos' maps to 'rank'
    assert core_entry.name == "John"
    assert core_entry.score == 1337
    assert core_entry.last_solve_time is None  # Not in sample, defaults to None
