import uuid
import secrets
from pathlib import Path
import json
import string

BASE_URL = "https://opencart.abstracta.us/"
REGISTER_URL = BASE_URL + "index.php?route=account/register"
LOGIN_URL = BASE_URL + "index.php?route=account/login"

ROOT = Path(__file__).resolve().parents[1]
ACCOUNT_FILE = ROOT / ".test_account.json"
SCREENSHOTS_DIR = ROOT / "screenshots"

def unique_email():
    domain = "example.com"
    return f"uts-systemtest-{uuid.uuid4().hex[:12]}@{domain}"

def unique_password():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(14))

def save_account(email, password):
    ACCOUNT_FILE.write_text(json.dumps({"email": email, "password": password}), encoding="utf-8")

def load_account():
    if not ACCOUNT_FILE.exists():
        raise AssertionError(
            "No test account found. Run the F2 registration feature first."
        )
    return json.loads(ACCOUNT_FILE.read_text(encoding="utf-8"))