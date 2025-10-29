import os, yaml, pathlib

_DEFAULTS = {
    "data": {"faq_path": "data/faq_dataset.json"},
    "retrieval": {
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "top_k": 3,
        "show_scores": True,
    },
    "llm": {"hf_fallback_model": "t5-small", "enable_reformulation": True},
    "ui": {
        "title": "KMS_lib — FAQ Assistant",
        "theme": "default",
        "enable_share": False,
        "server_name": "127.0.0.1",
        "server_port": 7860,
    },
}


def _read_yaml(path: pathlib.Path):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _env_override(cfg: dict) -> dict:
    faq = os.getenv("KMS_FAQ_PATH")
    emb = os.getenv("KMS_EMBEDDING_MODEL")
    topk = os.getenv("KMS_TOP_K")
    hf = os.getenv("KMS_HF_MODEL")
    share = os.getenv("KMS_SHARE")

    if faq:
        cfg["data"]["faq_path"] = faq
    if emb:
        cfg["retrieval"]["embedding_model"] = emb
    if topk:
        try:
            cfg["retrieval"]["top_k"] = int(topk)
        except ValueError:
            pass
    if hf:
        cfg["llm"]["hf_fallback_model"] = hf
    if share is not None:
        cfg["ui"]["enable_share"] = share.lower() in ("1", "true", "yes", "on")
    return cfg


def load_config() -> dict:
    root = pathlib.Path(__file__).resolve().parents[2]
    cfg_path = root / "src" / "config.yaml"
    cfg = {k: (v.copy() if isinstance(v, dict) else v) for k, v in _DEFAULTS.items()}
    user = _read_yaml(cfg_path)
    for k, v in user.items():
        if isinstance(v, dict) and k in cfg and isinstance(cfg[k], dict):
            cfg[k].update(v)
        else:
            cfg[k] = v
    cfg = _env_override(cfg)
    return cfg


_cfg = load_config()
FAQ_PATH = _cfg["data"]["faq_path"]
EMBEDDING_MODEL = _cfg["retrieval"]["embedding_model"]
TOP_K = _cfg["retrieval"]["top_k"]
SHOW_SCORES = _cfg["retrieval"]["show_scores"]
HF_FALLBACK_MODEL = _cfg["llm"]["hf_fallback_model"]
ENABLE_REFORM = _cfg["llm"]["enable_reformulation"]
UI = _cfg["ui"]