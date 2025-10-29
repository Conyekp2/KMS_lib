from __future__ import annotations
import json
from pathlib import Path
from typing import List, Tuple

from .retriever import Retriever

class FAQEngine:
    def __init__(self, faq_path, embedding_model: str):
        # Accept both str and Path
        self.faq_path = Path(faq_path)
        if not self.faq_path.exists():
            raise FileNotFoundError(f"FAQ file not found: {self.faq_path}")

        # Load and build corpus
        self.faq = json.loads(self.faq_path.read_text(encoding="utf-8"))

        # Build a simple corpus for retrieval: use answers as docs; store Q for debug
        self.corpus: List[str] = [item["answer"] for item in self.faq]
        self.questions: List[str] = [item["question"] for item in self.faq]

        self.retriever = Retriever(embedding_model)

    def answer(self, query: str, k: int = 3) -> Tuple[str, float, list]:
        idxs, scores = self.retriever.top_k(query, self.corpus, k=k)
        # pick best
        best_idx = idxs[0]
        best_score = scores[0]
        best_answer = self.corpus[best_idx]
        # debug payload: top-k Q/A pairs with scores
        debug = [
            {
                "rank": i + 1,
                "score": float(scores[i]),
                "question": self.questions[idxs[i]],
                "answer": self.corpus[idxs[i]],
            }
            for i in range(len(idxs))
        ]
        return best_answer, float(best_score), debug