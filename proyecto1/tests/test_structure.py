"""Verifica que la estructura de carpetas del proyecto sea la esperada."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATHS = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/routers/__init__.py",
    "app/routers/estimations.py",
    "app/services/__init__.py",
    "app/services/llm_service.py",
    "app/context/__init__.py",
    "app/context/examples.py",
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "README.md",
]


def test_required_files_exist():
    missing = [p for p in REQUIRED_PATHS if not (PROJECT_ROOT / p).is_file()]
    assert not missing, f"Faltan archivos/carpetas requeridos: {missing}"


def test_env_is_gitignored():
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore.splitlines(), ".env debe estar listado en .gitignore"


def test_context_has_at_least_two_examples():
    from app.context.examples import ESTIMATION_EXAMPLES

    assert len(ESTIMATION_EXAMPLES) >= 2
    for example in ESTIMATION_EXAMPLES:
        assert "meeting_summary" in example
        assert "estimation" in example
