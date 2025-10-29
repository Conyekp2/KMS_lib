import json
from pathlib import Path
from src.engines.retriever import Retriever

def test_topk_runs_with_small_model():
    faq = json.loads(Path("data/faq_dataset.json").read_text(encoding="utf-8"))
    candidates = [{"question": x["question"], "answer": x["answer"]} for x in faq]
    retriever = Retriever("sentence-transformers/all-MiniLM-L6-v2")
    results = retriever.topk("how to reserve a book", candidates, k=2)
    assert len(results) == 2
    assert isinstance(results[0][1], float)
