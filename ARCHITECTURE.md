# 📐 Architecture: Transcript Formatter

This document describes the internal architecture of the transcript formatter pipeline, which processes `.vtt` or `.txt` transcript files into clean Markdown documents, enriched with glossary substitutions and grammar review.

---

## 🧭 High-Level Flow

```
.vtt / .txt
  ↓
clean_input()
  ↓
group_by_speaker()
  ↓
split_paragraphs()
  ↓
apply_auto_fixes()
  ↓
apply_substitutions()
  ↓
check_paragraph()
  ↓
generate_summary() + generate_markdown()
```

---

## 🔧 Modules Overview

| Module               | Responsibility                                  |
|----------------------|--------------------------------------------------|
| `parser.py`          | Strip timestamps, normalize text lines          |
| `grouper.py`         | Aggregate utterances by speaker                 |
| `splitter.py`        | Segment speaker blocks into paragraphs          |
| `grammar_check.py`   | Auto-fix known issues, run grammar diagnostics  |
| `substituter.py`     | Load glossary and apply corrections             |
| `summarizer.py`      | Extract summary and action items (optional)     |
| `markdown_formatter.py` | Generate final `.md` transcript               |
| `pipeline_controller.py` | Orchestrate the full flow, CLI entrypoint   |

---

## 🧠 Design Decisions

- **Multi-pass processing** ensures clean grammar context
- **Glossary and ignore list** are JSON-backed and extensible
- **LanguageTool-based grammar engine** enables rule control
- **Only one grammar review file** is saved if issues are found
- **Markdown output** is designed for human readability and export

---

## 📁 Output File Structure

- `*.formatted.md` → Final transcript
- `*_grammar_review.txt` → Issues flagged by grammar engine
- `glossary_suggestions.txt` → Unknown tokens not in glossary