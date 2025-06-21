# markdown_formatter.py
# Converts parsed transcript data into a structured Markdown format.
# Now supports optional Summary and Action Items sections.

def generate_markdown(date, speaker_blocks, summary=None, action_items=None):
    """
    Create structured Markdown including meeting details, optional summary,
    optional action items, and full transcript.

    Parameters:
        date (str): Meeting date
        speaker_blocks (list): [(speaker_name, [paragraphs...])]
        summary (str or None): Summary paragraph(s)
        action_items (list of str): List of action items (optional)

    Returns:
        str: Full Markdown output
    """

    # Extract distinct speaker names from the transcript
    speakers = sorted(set(s for s, _ in speaker_blocks))

    lines = []

    # --- Meeting Header ---
    lines.append("## Meeting Details")
    lines.append(f"- **Date:** {date}")
    lines.append(f"- **Attendees:** {', '.join(speakers)}")
    lines.append("")

    # --- Optional Summary Section ---
    if summary:
        lines.append("## Summary")
        lines.append(summary.strip())
        lines.append("")

    # --- Optional Action Items ---
    if action_items:
        lines.append("## Action Items")
        for item in action_items:
            lines.append(f"- {item}")
        lines.append("")

    # --- Transcript Section ---
    lines.append("## Full Transcript")
    for speaker, paras in speaker_blocks:
        lines.append(f"**{speaker}:**")
        lines.extend(paras)
        lines.append("")  # Extra line break between speaker turns

    return '\n'.join(lines)
