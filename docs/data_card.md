# Data Card — KMS_lib

**Summary**: Synthetic datasets representing (1) metadata records, (2) user queries, and (3) FAQ pairs.  
**Motivation**: Enable safe public sharing and reproducible demonstrations without exposing any sensitive data.

## Datasets
- `metadata_samples.csv`: 50 synthetic records with fields such as title, author, year, discipline, keywords, abstract.
- `user_queries.csv`: 120 synthetic queries labeled by structure, specificity, and presumed intent.
- `faq_dataset.json`: ~25 Q/A pairs validated for clarity and consistency.

## Generation
- Data created by rules and templates; no real persons, institutions, or copyrighted content.
- Queries mimic common library search behaviors.

## Ethical Considerations
- No personally identifiable information.
- Not representative of any specific institution or community.
- Intended for method demonstration only.

## Recommended Use
- Replace or extend with your own exports when adapting the starter kit.
