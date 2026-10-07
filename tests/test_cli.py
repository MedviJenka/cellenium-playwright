import json
import pytest
from cellenium import cli


SETTINGS = {
    "GOOGLE_SHEETS": "https://docs.google.com/spreadsheets/d/sheet-id/edit",
    "OPENAI_MODEL": "model",
}


@pytest.fixture(autouse=True)
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name in [*SETTINGS, "CREDENTIALS_JSON", "OPENAI_API_KEY", "LOGFIRE_TOKEN", "TEST_HEADLESS"]:
        monkeypatch.delenv(name, raising=False)
    return tmp_path


def test_init_writes_env_and_protects_secrets(project):
    (project / ".gitignore").write_text("__pycache__/", encoding="utf-8")

    assert cli.main(["init", "--skip-browser"]) == 0

    assert "GOOGLE_SHEETS=" in (project / ".env").read_text(encoding="utf-8")
    assert (project / ".gitignore").read_text(encoding="utf-8").splitlines() == ["__pycache__/", ".env", "credentials.json"]


def test_init_keeps_existing_env_unless_forced(project):
    (project / ".env").write_text("GOOGLE_SHEETS=mine", encoding="utf-8")

    cli.main(["init", "--skip-browser"])
    assert (project / ".env").read_text(encoding="utf-8") == "GOOGLE_SHEETS=mine"

    cli.main(["init", "--skip-browser", "--force"])
    assert (project / ".env").read_text(encoding="utf-8") != "GOOGLE_SHEETS=mine"


def test_init_installs_chromium_with_current_interpreter(monkeypatch):
    commands = []
    monkeypatch.setattr(cli.subprocess, "run", lambda command: commands.append(command) or type("Done", (), {"returncode": 0})())

    assert cli.main(["init", "--with-deps"]) == 0

    assert commands == [[cli.sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"]]


def test_doctor_fails_on_fresh_template(capsys):
    cli.main(["init", "--skip-browser"])

    assert cli.main(["doctor", "--offline", "--skip-browser"]) == 1

    assert "empty settings: GOOGLE_SHEETS" in capsys.readouterr().out


def test_doctor_reports_service_account_email(project, monkeypatch, capsys):
    for name, value in SETTINGS.items():
        monkeypatch.setenv(name, value)
    (project / "credentials.json").write_text(json.dumps({"client_email": "bot@project.iam.gserviceaccount.com"}), encoding="utf-8")

    assert cli.main(["doctor", "--offline", "--skip-browser"]) == 0

    assert "share the spreadsheet with bot@project.iam.gserviceaccount.com" in capsys.readouterr().out


def test_doctor_fails_without_credentials(monkeypatch, capsys):
    for name, value in SETTINGS.items():
        monkeypatch.setenv(name, value)

    assert cli.main(["doctor", "--offline", "--skip-browser"]) == 1

    assert "credentials.json not found" in capsys.readouterr().out
