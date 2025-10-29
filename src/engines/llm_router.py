import subprocess
from typing import Optional
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LLMRouter:
    """
    Local-first LLM router.
    - Uses Ollama (if installed) with a small prompt for query reformulation.
    - Falls back to a small Hugging Face seq2seq model (no API keys required).
    """
    def __init__(self, hf_model: str):
        self.hf_tokenizer = AutoTokenizer.from_pretrained(hf_model)
        self.hf_model = AutoModelForSeq2SeqLM.from_pretrained(hf_model)

    @staticmethod
    def _ollama_available() -> bool:
        try:
            subprocess.run(["ollama", "list"], check=True, capture_output=True)
            return True
        except Exception:
            return False

    def _ollama_reformulate(self, text: str, model: str = "mistral") -> Optional[str]:
        prompt = (
            "Reformulate the following user query so it works well in a digital-library search. "
            "Keep it concise and specific.\n\n"
            f"Query: {text}\n\nReformulated:"
        )
        try:
            out = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, check=True, text=True
            )
            return out.stdout.strip()
        except Exception:
            return None

    def reformulate(self, text: str) -> str:
        if self._ollama_available():
            out = self._ollama_reformulate(text)
            if out:
                return out
        # HF fallback
        inputs = self.hf_tokenizer(f"Paraphrase the query for library search: {text}", return_tensors="pt")
        outputs = self.hf_model.generate(**inputs, max_new_tokens=64)
        return self.hf_tokenizer.decode(outputs[0], skip_special_tokens=True)