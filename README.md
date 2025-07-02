# Transcript Formatter

CLI tool to convert `.vtt` or `.txt` transcripts into structured Markdown. Includes speaker grouping, glossary substitution, grammar review, action item and summary extraction.

## ✅ Features

- 🎤 Speaker grouping
- ✂️ Paragraph splitting
- 📚 Glossary substitution and acronym logging
- 🧠 Grammar check (via LanguageTool)
- 🩹 Optional grammar autofix (e.g. spacing)
- ✅ Action item extraction with confidence scoring
- 📋 Summary generation (stubbed)
- 📄 Markdown output with logs

## 🚀 CLI Usage

```bash
python pipeline_controller.py input_file.vtt [options]
```

### 🔧 Options

| Flag                      | Description                                                    |
|---------------------------|----------------------------------------------------------------|
| `--with-summary`          | Enables summary **and** action item extraction                 |
| `--grammar-check`         | Performs grammar validation using LanguageTool (Java required)|
| `--autofix-grammar`       | Applies safe grammar fixes (e.g., spacing)                     |
| `--substitute-glossary`   | Replaces known glossary terms and flags unknown acronyms       |
| `--debug-actions`         | Prints match reasoning when action items are detected          |
| `--output-dir PATH`       | Where to save output Markdown and logs (default: `.`)          |

## 🧪 Example

```bash
python pipeline_controller.py meeting.vtt --with-summary --grammar-check --autofix-grammar --substitute-glossary --output-dir ./output
```