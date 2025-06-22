import re

def split_paragraphs(text):
    """
    Split a speaker's text block into sub-paragraphs based on length, topic shifts,
    and sentence count — with less aggressive behavior for casual conversation.
    """
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    chunks = []
    buffer = []

    for sentence in sentences:
        sentence = sentence.strip()
        buffer.append(sentence)

        # Trigger a paragraph break if:
        total_length = sum(len(s) for s in buffer)
        if (
            len(buffer) >= 4 or
            total_length >= 300 or
            any(p in sentence for p in [
                "Next", "On another note", "That said", "One more thing", "Anyway", "So, the other thing"
            ])
        ):
            chunks.append(' '.join(buffer).strip())
            buffer = []

    if buffer:
        chunks.append(' '.join(buffer).strip())

    return chunks
