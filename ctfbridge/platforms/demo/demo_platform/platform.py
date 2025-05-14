import copy
from pathlib import Path

import yaml

from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.models.submission import SubmissionResult

CURRENT_DIR = Path(__file__).resolve().parent
CHALLENGES_DIR = CURRENT_DIR / "challenges"


class DemoPlatform:
    def __init__(self):
        self.challenges: list[Challenge] = []
        self.flag_map: dict[int, str] = {}
        self.attachments_map = {}
        self._load_challenges()

    def load_challenge_from_yaml(self, path: Path) -> Challenge:
        with open(path / "challenge.yaml") as f:
            data = yaml.safe_load(f)

        challenge_id = len(self.challenges) + 1

        attachments = []
        for rel_path in data.get("files", []):
            file_path = path / rel_path
            if not file_path.exists():
                raise FileNotFoundError(f"Missing file: {file_path}")

            url = f"/challenges/{challenge_id}/attachments/{file_path.name}"
            attachments.append(Attachment(name=file_path.name, url=url))

            self.attachments_map[url] = file_path

        challenge = Challenge(
            id=challenge_id,
            name=data["name"],
            category=data["category"],
            value=data["value"],
            description=data["description"],
            attachments=attachments,
            solved=False,
        )

        self.flag_map[challenge.id] = data["flag"]

        return challenge

    def _load_challenges(self):
        for category_dir in CHALLENGES_DIR.iterdir():
            if category_dir.is_dir():
                for challenge_dir in category_dir.iterdir():
                    if (challenge_dir / "challenge.yaml").exists():
                        challenge = self.load_challenge_from_yaml(challenge_dir)
                        self.challenges.append(challenge)

    def get_all_challenges(self) -> list[Challenge]:
        return [copy.deepcopy(ch) for ch in self.challenges]

    def get_challenge_by_id(self, challenge_id: int) -> Challenge:
        for ch in self.challenges:
            if ch.id == challenge_id:
                return copy.deepcopy(ch)
        raise ValueError(f"No challenge with id {challenge_id}")

    def submit_flag(self, challenge_id: int, flag: str) -> SubmissionResult:
        expected = self.flag_map[challenge_id]
        if expected is None:
            raise ValueError("Challenge not found.")

        if flag.strip() == expected:
            self.get_challenge_by_id(challenge_id).solved = True
            return SubmissionResult(correct=True, message="Correct!")
        else:
            return SubmissionResult(correct=False, message="Wrong!")
