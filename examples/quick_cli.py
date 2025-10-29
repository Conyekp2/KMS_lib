import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from engines.faq_engine import FAQEngine
from app.config import FAQ_PATH, EMBEDDING_MODEL

if __name__ == "__main__":
    eng = FAQEngine(FAQ_PATH, EMBEDDING_MODEL)
    q = input("Ask: ")
    ans, score, dbg = eng.answer(q, k=3)
    print("\nAnswer:", ans)
    print("Score:", round(score, 3))
