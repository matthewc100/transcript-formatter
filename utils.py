# utils.py
# Utility functions like file naming, date extraction, saving files

import re
from datetime import datetime
from pathlib import Path

def extract_date_from_filename(filename):
    match = re.search(r'GMT(\d{8})', filename)
    if match:
        dt = datetime.strptime(match.group(1), "%Y%m%d")
        return dt.strftime("%B %d, %Y").replace(" 0", " ")
    return "Unknown"

def save_output(input_path, content):
    output_path = Path(input_path).with_suffix(".formatted.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved to: {output_path}")
