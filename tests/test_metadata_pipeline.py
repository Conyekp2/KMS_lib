from pathlib import Path
import pandas as pd

def test_metadata_file_exists():
    data_path = Path("data/metadata_samples.csv")
    assert data_path.exists(), "metadata_samples.csv is missing"

def test_metadata_schema_minimal():
    df = pd.read_csv("data/metadata_samples.csv")
    required = {"id","title","author","year","discipline","keywords","abstract"}
    assert required.issubset(df.columns), f"Missing columns: {required - set(df.columns)}"
