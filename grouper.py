import re

def group_by_speaker(lines):
    """
    Aggregate transcript lines into blocks grouped by speaker.
    If the same speaker appears multiple times in a row, merge their lines.
    """
    grouped = []
    current_speaker = None
    buffer = []

    for line in lines:
        match = re.match(r'^([A-Za-z][\w\s\.\-]+):\s*(.*)', line)
        if match:
            speaker, text = match.groups()
            speaker = speaker.strip()

            if speaker != current_speaker:
                # Speaker changed — flush previous
                if current_speaker and buffer:
                    grouped.append((current_speaker, ' '.join(buffer)))
                    buffer = []
                current_speaker = speaker

            # Append text whether speaker changed or not
            buffer.append(text.strip())
        else:
            # Continuation of previous speaker
            buffer.append(line.strip())

    # Final flush
    if current_speaker and buffer:
        grouped.append((current_speaker, ' '.join(buffer)))

    return grouped
