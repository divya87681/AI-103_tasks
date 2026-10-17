from src.cli import run

def test_placeholder_is_not_claimed_verified():
    assert run("sample")["status"] == "NOT_VERIFIED"
