from pathlib import Path
from src.engines.faq_engine import FAQEngine

def test_faq_engine_basic():
    engine = FAQEngine(Path("data/faq_dataset.json"), "sentence-transformers/all-MiniLM-L6-v2")
    ans, score, dbg = engine.answer("Where is the final project template?", k=3)
    assert isinstance(ans, str) and ans
    assert 0.0 <= score <= 1.0
    assert isinstance(dbg, list) and len(dbg) >= 1
