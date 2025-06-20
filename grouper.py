# grouper.py
# Groups transcript lines under their corresponding speaker

import re

def group_by_speaker(lines):
    grouped = []
    speaker = None
    buffer = []

    for line in lines:
        match = re.match(r'^([A-Za-z][\w\s\.\-]+):\s*(.*)', line)
        if match:
            if speaker and buffer:
                grouped.append((speaker, ' '.join(buffer)))
                buffer = []
            speaker, text = match.groups()
            buffer.append(text.strip())
        else:
            buffer.append(line.strip())

    if speaker and buffer:
        grouped.append((speaker, ' '.join(buffer)))

    return grouped
