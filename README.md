# 📝 Transcript Formatter (Markdown Output)

This Python project converts raw meeting transcripts (e.g., from `.txt` or `.vtt` files) into clean, structured **Markdown documents**.

It performs:
- Timestamp and numeric sequence removal
- Speaker grouping and turn detection
- Paragraph splitting based on heuristics
- Markdown formatting with metadata (date, attendees)

## 🧱 Project Structure

```
transcript_formatter/
├── main.py
├── parser.py
├── grouper.py
├── splitter.py
├── markdown_formatter.py
├── utils.py
└── README.md
```

## 🚀 Installation

> Recommended: Use Python 3.9 or newer.

### 1. Clone the repository

```bash
git clone https://github.com/your-org/transcript-formatter.git
cd transcript-formatter
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements

No external libraries are needed for basic Markdown output.

## 🧪 Usage

```bash
python main.py path/to/your_transcript.txt
```

- Output will be saved as: `your_transcript.formatted.md`
