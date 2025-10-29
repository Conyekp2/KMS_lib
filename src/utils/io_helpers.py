from pathlib import Path

def ensure_exists(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
