# 📝 Transcript Formatter (Markdown Output)

This Python project converts raw meeting transcripts (e.g., `.txt` or `.vtt` files) into clean, structured **Markdown documents**.

It performs:
- Timestamp and numeric sequence removal
- Speaker grouping and turn detection
- Paragraph splitting using `nltk` for more natural speech handling
- Markdown formatting with metadata (date, attendees)
- *(Optional)* Summary and action item extraction
- *(Optional)* Glossary-based substitutions for domain-specific corrections
- *(Optional)* Output file redirection to a specific folder
- *(Optional)* Acronym review, suggestion tracking, and glossary promotion

---

## 🧱 Project Structure

```
transcript_formatter/
├── main.py                      # CLI entry point
├── parser.py                    # Cleans input
├── grouper.py                   # Groups by speaker
├── splitter.py                  # Splits long turns
├── markdown_formatter.py        # Builds Markdown
├── summarizer.py                # Summary and action items
├── substituter.py               # Glossary-based substitutions
├── glossary_stats.py            # Tracks unknown acronym frequency
├── promote_to_glossary.py       # (Deprecated - merged)
├── manage_suggestions.py        # CLI tool to promote to glossary or ignore
├── glossary.json                # Substitution glossary
├── ignore_acronyms.json         # Terms to skip during suggestion
├── sort_glossary.py             # Sorts glossary entries
├── acronym_stats.json           # Frequency of unknown terms (auto-generated)
├── glossary_suggestions.txt     # Context log of unknown terms (auto-generated)
└── README.md
```

---

## 🚀 Installation

> Requires Python 3.9 or newer.

```bash
pip install nltk
python -m nltk.downloader punkt
```

---

## 🧪 CLI Usage

```bash
python main.py <input_file> [--with-summary] [--debug-no-summary] [--substitute-glossary] [--output-dir DIR]
```

### Example:

```bash
python main.py myfile.vtt --with-summary --substitute-glossary --output-dir ./output
```

---

## 🧠 Glossary and Suggestion Management

### Track unknowns and review them:

```bash
python main.py transcript.vtt --substitute-glossary
```

- This will update:
  - `glossary_suggestions.txt` — with context
  - `acronym_stats.json` — with frequency

### Promote unknown terms with 1-key selection:

```bash
python manage_suggestions.py
```

- `[p]` Promote to glossary
- `[i]` Add to ignore list
- `[s]` Skip for now

---

## 🛠 Features Roadmap

- [x] Summary and action item scaffolding
- [x] Glossary-based substitution
- [x] Acronym context logging + frequency tracking
- [x] Promote-to-glossary + ignore flow
- [x] Optional grammar autofix with `--autofix-grammar`
- [ ] `.docx` or `.pdf` export
- [ ] NLP-based topic detection
- [ ] Git-integrated glossary sync

---

## 👥 Maintainers

- Matt Coblentz (@matthewc100)
- OpenAI GPT Architecture Assistant
