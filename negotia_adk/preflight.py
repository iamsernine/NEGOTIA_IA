from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Tuple


KEY_NAMES = ["GOOGLE_API_KEY", "GEMINI_API_KEY", "GOOGLE_AI_API_KEY"]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def configured_key_name() -> str | None:
    return next((name for name in KEY_NAMES if os.getenv(name)), None)


def configured_key_value() -> str:
    key_name = configured_key_name()
    return os.getenv(key_name, "") if key_name else ""


def selected_model() -> str:
    return os.getenv("NEGOTIA_GEMINI_MODEL", "gemini-2.5-flash")


def preflight_gemini_access() -> Tuple[bool, str]:
    if os.getenv("NEGOTIA_SKIP_PREFLIGHT") == "1":
        return True, "Gemini preflight skipped because NEGOTIA_SKIP_PREFLIGHT=1."

    key_name = configured_key_name()
    if not key_name:
        return False, "Gemini API key missing. Add GOOGLE_API_KEY to .env."

    api_key = configured_key_value()
    if not api_key.startswith("AIza"):
        return (
            False,
            "The key in .env does not look like a Google AI Studio Gemini API key. "
            "Google AI Studio keys usually begin with AIza.",
        )

    model = selected_model()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Return only: OK"}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 8},
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response.read()
        return True, f"Gemini preflight OK using {key_name} with {model}."
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        if "PERMISSION_DENIED" in detail or exc.code == 403:
            return (
                False,
                "Gemini preflight failed: 403 PERMISSION_DENIED. "
                "The Google project or API key is denied access to Gemini. "
                "Create a valid Google AI Studio Gemini API key and put it in .env. "
                "If the key is valid but model access is limited, try NEGOTIA_GEMINI_MODEL=gemini-1.5-flash.",
            )
        return False, f"Gemini preflight failed: HTTP {exc.code} {exc.reason}. {detail[:800]}"
    except Exception as exc:
        return False, f"Gemini preflight failed: {exc}"

