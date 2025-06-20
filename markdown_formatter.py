# markdown_formatter.py
# Converts parsed transcript data into a clean Markdown format

def generate_markdown(date, speaker_blocks):
    speakers = sorted(set(s for s, _ in speaker_blocks))
    lines = [
        "## Meeting Details",
        f"- **Date:** {date}",
        f"- **Attendees:** {', '.join(speakers)}",
        "",
        "## Full Transcript"
    ]

    for speaker, paras in speaker_blocks:
        lines.append(f"**{speaker}:**")
        lines.extend(paras)
        lines.append("")

    return '\n'.join(lines)
