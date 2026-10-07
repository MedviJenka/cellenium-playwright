"""
cellenium command line.

    cellenium init     scaffold .env, protect secrets in .gitignore, install Chromium
    cellenium doctor   verify configuration, Google Sheets access, and the browser
"""
import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from importlib.resources import files
from pathlib import Path
from pydantic import ValidationError
from cellenium.settings import Settings


ENV_FILE = Path(".env")
GITIGNORE = Path(".gitignore")
SECRETS = (".env", "credentials.json")
OPTIONAL_FIELDS = {"OPENAI_API_KEY", "LOGFIRE_TOKEN"}


def _ok(message: str) -> None:
    print(f"  [ok]   {message}")


def _fail(message: str, hint: str | None = None) -> None:
    print(f"  [fail] {message}")
    if hint:
        print(f"         -> {hint}")


# ------------------------------ #
#              init              #
# ------------------------------ #

def _write_env(force: bool) -> None:
    if ENV_FILE.exists() and not force:
        _ok(f"{ENV_FILE} already exists (use --force to overwrite)")
        return
    ENV_FILE.write_text(files("cellenium").joinpath("templates/env.template").read_text(encoding="utf-8"), encoding="utf-8")
    _ok(f"wrote {ENV_FILE}")


def _protect_secrets() -> None:
    existing = GITIGNORE.read_text(encoding="utf-8").splitlines() if GITIGNORE.exists() else []
    missing = [entry for entry in SECRETS if entry not in existing]
    if not missing:
        _ok(f"{GITIGNORE} already ignores {', '.join(SECRETS)}")
        return
    with GITIGNORE.open("a", encoding="utf-8") as handle:
        if existing and existing[-1].strip():
            handle.write("\n")
        handle.write("\n".join(missing) + "\n")
    _ok(f"added {', '.join(missing)} to {GITIGNORE}")


def _install_browser(with_deps: bool) -> bool:
    command = [sys.executable, "-m", "playwright", "install", "chromium"]
    if with_deps:
        command.insert(4, "--with-deps")
    print(f"  installing Chromium: {' '.join(command[1:])}")
    if subprocess.run(command).returncode != 0:
        _fail("Chromium install failed", "rerun the command above to see the error")
        return False
    _ok("Chromium installed")
    return True


def init(args: argparse.Namespace) -> int:
    print("cellenium init")
    _write_env(args.force)
    _protect_secrets()
    if not args.skip_browser and not _install_browser(args.with_deps):
        return 1
    print(
        "\nnext steps:\n"
        "  1. fill in .env\n"
        "  2. save your Google service-account key as credentials.json\n"
        "  3. share the spreadsheet with the service account's client_email (Viewer)\n"
        "  4. run `cellenium doctor`"
    )
    return 0


# ------------------------------ #
#             doctor             #
# ------------------------------ #

def _check_config() -> Settings | None:
    if not ENV_FILE.exists():
        print(f"  [info] no {ENV_FILE} in {Path.cwd()} - reading environment variables only")
    try:
        config = Settings()
    except ValidationError as error:
        names = ", ".join(str(e["loc"][0]) for e in error.errors())
        _fail(f"settings invalid: {names}", "set them in .env or as environment variables (`cellenium init` writes a template)")
        return None
    blank = [name for name, value in config.model_dump().items() if value == "" and name not in OPTIONAL_FIELDS]
    if blank:
        _fail(f"empty settings: {', '.join(blank)}", "fill them in .env")
        return None
    _ok("settings loaded")
    return config


def _check_credentials(config: Settings) -> bool:
    path = config.CREDENTIALS_JSON
    if not path.exists():
        _fail(f"{path} not found", "download a service-account key from Google Cloud Console > IAM > Service Accounts")
        return False
    try:
        email = json.loads(path.read_text(encoding="utf-8"))["client_email"]
    except (ValueError, KeyError):
        _fail(f"{path} is not a service-account key (no client_email)")
        return False
    _ok(f"{path} found - share the spreadsheet with {email}")
    return True


def _check_sheet(config: Settings) -> bool:
    import gspread

    try:
        spreadsheet = gspread.service_account(filename=str(config.CREDENTIALS_JSON)).open_by_url(config.GOOGLE_SHEETS)
        screens = [worksheet.title for worksheet in spreadsheet.worksheets()]
    except Exception as error:
        _fail(f"cannot open GOOGLE_SHEETS: {type(error).__name__}: {error}", "check the URL and that the sheet is shared with the service account")
        return False
    _ok(f"spreadsheet opened - screens: {', '.join(screens) or '(none)'}")
    return True


def _check_browser() -> bool:
    from playwright.sync_api import Error, sync_playwright

    try:
        with sync_playwright() as playwright:
            playwright.chromium.launch(headless=True).close()
    except Error as error:
        _fail(f"Chromium does not launch: {str(error).splitlines()[0]}", "run `cellenium init` or `playwright install chromium`")
        return False
    _ok("Chromium launches")
    return True


def doctor(args: argparse.Namespace) -> int:
    print("cellenium doctor")
    checks: list[Callable[[], bool]] = []
    config = _check_config()
    if config:
        checks.append(lambda: _check_credentials(config) and (args.offline or _check_sheet(config)))
    if not args.skip_browser:
        checks.append(_check_browser)
    results = [check() for check in checks]
    healthy = config is not None and all(results)
    print("\nall checks passed" if healthy else "\nsome checks failed")
    return 0 if healthy else 1


# ------------------------------ #
#           entry point          #
# ------------------------------ #

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cellenium", description="Set up and verify a cellenium project.")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="scaffold .env, protect secrets, install Chromium")
    init_parser.add_argument("--force", action="store_true", help="overwrite an existing .env")
    init_parser.add_argument("--skip-browser", action="store_true", help="do not install Chromium")
    init_parser.add_argument("--with-deps", action="store_true", help="also install Chromium's system libraries (Linux/CI)")
    init_parser.set_defaults(handler=init)

    doctor_parser = commands.add_parser("doctor", help="verify configuration, sheet access, and the browser")
    doctor_parser.add_argument("--offline", action="store_true", help="skip opening the Google Sheet")
    doctor_parser.add_argument("--skip-browser", action="store_true", help="skip launching Chromium")
    doctor_parser.set_defaults(handler=doctor)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
