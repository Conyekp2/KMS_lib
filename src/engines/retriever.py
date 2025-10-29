from __future__ import annotations
from typing import Iterable, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer, util


class Retriever:
    """
    Minimal dense retriever using SentenceTransformers.
    Provides both top_k() and alias topk() for convenience.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def top_k(self, query: str, corpus: Iterable[str], k: int = 3) -> Tuple[List[int], List[float]]:
        """
        Compute cosine similarity between query and corpus embeddings
        and return indices of top-k docs plus their scores.
        """
        q_emb = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
        c_list = list(corpus)
        c_emb = self.model.encode(c_list, convert_to_tensor=True, normalize_embeddings=True)

        sims = util.cos_sim(q_emb, c_emb).cpu().numpy().flatten()
        k = max(1, min(k, len(c_list)))
        idxs = np.argsort(-sims)[:k]
        scores = sims[idxs]

        return idxs.tolist(), scores.astype(float).tolist()

    def topk(self, query: str, corpus: Iterable[dict], k: int = 3):
        """
        Compatibility wrapper for tests.
        Returns list of (index, score) tuples instead of separate lists.
        """
        if corpus and isinstance(corpus[0], dict) and "answer" in corpus[0]:
            docs = [c["answer"] for c in corpus]
        else:
            docs = corpus

        idxs, scores = self.top_k(query, docs, k)
        return list(zip(idxs, scores))
