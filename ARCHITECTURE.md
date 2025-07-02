# Architecture Overview

## Pipeline Flow

1. `clean_input()` - remove VTT markup
2. `group_by_speaker()` - group lines
3. `split_paragraphs()` - sentence splitting
4. `apply_auto_fixes()` - safe grammar fixes
5. `apply_substitutions()` - glossary term replacement
6. `check_paragraph()` - grammar checker
7. `extract_summary()` - basic summary logic
8. `extract_action_items()` - keyword or NLP matching
9. `generate_markdown()` - final output

## Modular Design

| Module              | Function                          |
|---------------------|-----------------------------------|
| `summarizer.py`     | Routes to summary and action logic|
| `action_extractor.py`| Extracts to-do's from speaker text|
| `summary_extractor.py`| Placeholder for summarization    |