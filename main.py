# main.py
# Entry point for processing transcript files into structured Markdown output

from parser import clean_input
from grouper import group_by_speaker
from splitter import split_paragraphs
from markdown_formatter import generate_markdown
from utils import extract_date_from_filename, save_output
from summarizer import generate_summary, extract_action_items  # ✅ Step 1: Import

def process_transcript(file_path):
    # Step 1: Clean and strip transcript input
    raw_lines = clean_input(file_path)

    # Step 2: Group speech by speaker
    speaker_blocks = group_by_speaker(raw_lines)

    # Step 3: Paragraph splitting within each speaker block
    refined_blocks = [(s, split_paragraphs(t)) for s, t in speaker_blocks]

    # Step 4: Extract meeting date from filename
    date = extract_date_from_filename(file_path)

    # ✅ Step 5: Add summary and action items here (replace with CLI flag later)
    include_summary = True  # Toggle this if/when you add command-line options

    if include_summary:
        summary = generate_summary(refined_blocks)
        action_items = extract_action_items(refined_blocks)
    else:
        summary = None
        action_items = []

    # Step 6: Generate final Markdown (now includes optional sections)
    md = generate_markdown(date, refined_blocks, summary, action_items)

    # Step 7: Save result to file
    save_output(file_path, md)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py transcript.txt")
    else:
        process_transcript(sys.argv[1])
