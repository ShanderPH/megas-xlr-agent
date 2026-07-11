import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    for name in (".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov"):
        shutil.rmtree(ROOT / name, ignore_errors=True)
    for path in ROOT.rglob("__pycache__"):
        if ".venv" not in path.parts:
            shutil.rmtree(path, ignore_errors=True)
    (ROOT / ".coverage").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
