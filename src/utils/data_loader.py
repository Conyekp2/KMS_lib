from pathlib import Path
import pandas as pd
import json

def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
