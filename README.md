# Transcript Formatter

A modular, CLI-driven Python tool to convert transcript files (e.g., `.vtt`, `.txt`) into clean, structured Markdown output. Designed for enterprise use, it supports glossary-based substitutions, grammar correction, and optional summarization.

---

## 🔧 Features

- ✅ Converts `.vtt` and `.txt` transcripts to Markdown
- ✅ Aggregates by speaker and paragraphs
- ✅ Applies glossary-based substitutions (e.g., "5 9" → "Five9")
- ✅ Optional grammar correction using LanguageTool
- ✅ Optional summary and action item extraction
- ✅ Outputs Markdown and optional review logs

---

## 🧠 Architecture

```
pipeline_controller.py
 ├── clean_input()           # Strip VTT formatting
 ├── group_by_speaker()      # Aggregate by speaker
 ├── split_paragraphs()      # Sentence/paragraph splitting
 ├── apply_auto_fixes()      # Safe grammar rules (e.g., spacing)
 ├── apply_substitutions()   # Glossary fixes
 ├── check_paragraph()       # Grammar review using LanguageTool
 ├── generate_summary()      # Optional summary/actions
 └── generate_markdown()     # Final Markdown output
```

---

## 🚀 Usage

```bash
python pipeline_controller.py your_transcript.vtt --grammar-check --substitute-glossary --with-summary --output-dir ./output
```

### CLI Options

| Flag                 | Description                                 |
|----------------------|---------------------------------------------|
| `--grammar-check`     | Enable grammar checking (after auto-fix)    |
| `--substitute-glossary` | Apply glossary substitutions                |
| `--with-summary`       | Include summary and action item section     |
| `--output-dir`         | Output location for .md and logs (default: `.`) |

---

## 📄 Output Files

- `*.formatted.md` — final transcript
- `*_grammar_review.txt` — grammar suggestions (only if issues found)
- `glossary_suggestions.txt` — acronyms/tokens not in the glossary

---

## 🔭 Next Considerations

- [ ] Interactive glossary manager (promote/ignore from review file)
- [ ] Grammar rule toggles (`--log-typos`, `--log-style`)
- [ ] Markdown formatting themes or templates
- [ ] Add acronym context window around glossary hits
- [ ] Auto-promote frequently corrected glossary entries
- [ ] Optional `.docx` export
- [ ] Slack or GitHub bot integration for uploads
- [ ] Web UI for uploading transcripts and downloading output
- [ ] Batch mode / directory processing

---

## 🧪 Requirements

- Python 3.8+
- `language-tool-python`
- Optional: `nltk` (for smarter paragraph splitting)

---

## 🙌 Acknowledgments

Built with care and collaboration — transcript processing reimagined.