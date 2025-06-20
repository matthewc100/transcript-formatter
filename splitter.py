# splitter.py
# Applies heuristic rules to break up long paragraphs within a single speaker turn

import re

def split_paragraphs(text):
    sentences = re.split(r'(?<=\.)\s+(?=[A-Z])', text)
    chunks = []
    buffer = []

    for sentence in sentences:
        buffer.append(sentence)
        if len(buffer) >= 2 or any(phrase in sentence for phrase in ['Next', 'That said', 'On another note']):
            chunks.append(' '.join(buffer).strip())
            buffer = []

    if buffer:
        chunks.append(' '.join(buffer).strip())

    return chunks
