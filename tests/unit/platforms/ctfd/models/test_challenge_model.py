import pytest
from pydantic import ValidationError

from ctfbridge.models.challenge import Attachment as CoreAttachment
from ctfbridge.models.challenge import Challenge as CoreChallenge
from ctfbridge.models.submission import SubmissionResult as CoreSubmissionResult
from ctfbridge.platforms.ctfd.models.challenge import CTFdChallenge, CTFdSubmission

sample_ctfd_challenge_data_full = {
    "success": True,
    "data": {
        "id": 557,
        "name": "Attachments",
        "value": 500,
        "initial": 500,
        "decay": 85,
        "minimum": 100,
        "description": "Challenges may provide attachments. These often include important information required to solve the challenge.\r\n\r\nCan you download the attached file and find the flag?",
        "connection_info": None,
        "category": "Tutorial",
        "state": "visible",
        "max_attempts": 0,
        "type": "dynamic",
        "type_data": {
            "id": "dynamic",
            "name": "dynamic",
            "templates": {
                "create": "/plugins/dynamic_challenges/assets/create.html",
                "update": "/plugins/dynamic_challenges/assets/update.html",
                "view": "/plugins/dynamic_challenges/assets/view.html",
            },
            "scripts": {
                "create": "/plugins/dynamic_challenges/assets/create.js",
                "update": "/plugins/dynamic_challenges/assets/update.js",
                "view": "/plugins/dynamic_challenges/assets/view.js",
            },
        },
        "solves": 1,
        "solved_by_me": False,
        "attempts": 0,
        "files": ["/play/files/6bf59172065beb069515172363a6526d/flag.txt?token=..."],
        "tags": ["Challenge ID: nhojqlyj"],
        "hints": [],
        "view": '<div class="modal-dialog" role="document">...</div>',
    },
}

sample_ctfd_challenge_data_minimal = {
    "id": 557,
    "type": "dynamic",
    "name": "Attachments",
    "value": 500,
    "solves": 1,
    "solved_by_me": False,
    "category": "Tutorial",
    "tags": [{"value": "beginner"}],
    "template": "/plugins/dynamic_challenges/assets/view.html",
    "script": "/plugins/dynamic_challenges/assets/view.js",
}


def test_ctfd_challenge_parse_full():
    chal = CTFdChallenge(**sample_ctfd_challenge_data_full["data"])
    assert chal.id == 557
    assert chal.name == "Attachments"
    assert chal.value == 500
    assert chal.category == "Tutorial"
    assert chal.description.startswith("Challenges may provide attachments.")
    assert chal.connection_info is None
    assert chal.solved_by_me is False
    assert chal.tags == ["Challenge ID: nhojqlyj"]
    assert len(chal.files) == 1
    assert "flag.txt" in chal.files[0]


def test_ctfd_challenge_parse_minimal():
    chal = CTFdChallenge(**sample_ctfd_challenge_data_minimal)
    assert chal.id == 557
    assert chal.name == "Attachments"
    assert chal.description is None
    assert chal.tags == [{"value": "beginner"}]
    assert chal.files == []
    assert chal.solved_by_me is False


def test_ctfd_challenge_to_core_model_full():
    ctfd_chal = CTFdChallenge(**sample_ctfd_challenge_data_full["data"])
    core_chal = ctfd_chal.to_core_model()

    assert isinstance(core_chal, CoreChallenge)
    assert core_chal.id == "557"
    assert core_chal.name == "Attachments"
    assert core_chal.value == 500
    assert core_chal.category == "Tutorial"
    assert core_chal.categories == ["Tutorial"]
    assert core_chal.description.startswith("Challenges may provide attachments.")
    assert core_chal.solved is False

    assert len(core_chal.attachments) == 1
    assert "flag.txt" in core_chal.attachments[0].name
    assert "/play/files/" in core_chal.attachments[0].download_info.url

    assert core_chal.tags == ["Challenge ID: nhojqlyj"]


def test_ctfd_challenge_to_core_model_minimal():
    ctfd_chal = CTFdChallenge(**sample_ctfd_challenge_data_minimal)
    core_chal = ctfd_chal.to_core_model()

    assert isinstance(core_chal, CoreChallenge)
    assert core_chal.id == "557"
    assert core_chal.name == "Attachments"
    assert core_chal.category == "Tutorial"
    assert core_chal.description is None
    assert core_chal.attachments == []
    assert core_chal.tags == ["beginner"]
    assert core_chal.solved is False


def test_ctfd_challenge_to_core_model_no_category():
    data = sample_ctfd_challenge_data_minimal.copy()
    data.pop("category", None)
    with pytest.raises(ValidationError):
        CTFdChallenge(**data)


# Test data for CTFdSubmission
sample_ctfd_submission_correct = {"status": "correct", "message": "Correct"}
sample_ctfd_submission_incorrect = {"status": "incorrect", "message": "Incorrect"}
sample_ctfd_submission_already_solved = {
    "status": "already_solved",
    "message": "You already solved this",
}
sample_ctfd_submission_error_no_status = {
    "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again. You have requested this URI [/api/v1/challenges/attempt] but did you mean /api/v1/challenges/attempt or /api/v1/challenges/types or /api/v1/challenges/<challenge_id> ?"
}


def test_ctfd_submission_parse():
    sub_correct = CTFdSubmission(**sample_ctfd_submission_correct)
    assert sub_correct.status == "correct"
    assert sub_correct.message == "Correct"

    sub_no_status = CTFdSubmission(**sample_ctfd_submission_error_no_status)
    assert sub_no_status.status is None
    assert "The requested URL was not found on the server" in sub_no_status.message


def test_ctfd_submission_to_core_model():
    sub_correct_ctfd = CTFdSubmission(**sample_ctfd_submission_correct)
    core_sub_correct = sub_correct_ctfd.to_core_model()
    assert isinstance(core_sub_correct, CoreSubmissionResult)
    assert core_sub_correct.correct is True
    assert core_sub_correct.message == "Correct"

    sub_incorrect_ctfd = CTFdSubmission(**sample_ctfd_submission_incorrect)
    core_sub_incorrect = sub_incorrect_ctfd.to_core_model()
    assert core_sub_incorrect.correct is False
    assert core_sub_incorrect.message == "Incorrect"

    sub_already_solved_ctfd = CTFdSubmission(**sample_ctfd_submission_already_solved)
    core_sub_already_solved = sub_already_solved_ctfd.to_core_model()
    assert core_sub_already_solved.correct is False
    assert core_sub_already_solved.message == "You already solved this"

    sub_error_ctfd = CTFdSubmission(**sample_ctfd_submission_error_no_status)
    core_sub_error = sub_error_ctfd.to_core_model()
    assert core_sub_error.correct is False
    assert "The requested URL was not found on the server" in core_sub_error.message
