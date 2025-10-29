# Data Documentation

All datasets in this folder are **synthetic**, created to mimic typical academic usage patterns.
They contain **no personal or institutional data** and may be safely shared and reused.

## Files
- `faq_dataset.json` — curated FAQ pairs for a library / academic support context.
- `metadata_samples.csv` — simulated bibliographic/metadata records (titles, subjects, levels).
- `user_queries.csv` — synthetic user search queries (short/ambiguous + long/goal-oriented).

## Intended Use
- Educational demos (NLP pipelines, retrieval, chatbot prototypes)
- Benchmarking lightweight semantic search
- Reproducible research & teaching materials

## Minimal Schemas

### `faq_dataset.json` (example item)
```json
{
  "question": "Where can I find the final report template?",
  "answer": "You can download the final-year report template from the repository's 'Templates' section.",
  "intent": "templates_access",
  "policy_tag": "open_resource",
  "nuance_tags": ["register:neutral","politeness:medium"]
}

