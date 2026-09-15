"""Valida que la estructura de carpetas del proyecto sea la esperada."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXPECTED_FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/routers/__init__.py",
    "app/routers/estimations.py",
    "app/services/__init__.py",
    "app/services/llm_service.py",
    "app/context/__init__.py",
    "app/context/examples.py",
    "pyproject.toml",
    ".env.example",
    ".gitignore",
    "README.md",
]


def test_expected_files_exist():
    missing = [f for f in EXPECTED_FILES if not (ROOT / f).is_file()]
    assert not missing, f"Faltan archivos/carpetas esperados: {missing}"


def test_env_is_gitignored():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore


def test_env_example_has_no_real_keys():
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "sk-" not in env_example
