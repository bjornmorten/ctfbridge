from ctfbridge.models.scoreboard import ScoreboardEntry


def parse_scoreboard_entry(data: dict) -> ScoreboardEntry:
    return ScoreboardEntry(
        name=str(data["name"]),
        score=int(data["score"]),
        rank=int(data["pos"]),
    )
