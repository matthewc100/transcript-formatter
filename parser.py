# parser.py
# Cleans transcript input lines by removing timestamps and numeric markers

import re

def clean_input(file_path):
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = line.strip()

        # ✅ Suppress WebVTT header
        if line.upper().startswith("WEBVTT"):
            continue

        # Skip timestamps and numeric markers
        if re.match(r'\d{2}:\d{2}:\d{2}', line) or '-->' in line:
            continue
        if re.match(r'^\d+$', line):
            continue

        cleaned.append(line)

    return cleaned

