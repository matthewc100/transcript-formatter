# main.py
# Entry point for processing transcript files into structured Markdown output

from parser import clean_input
from grouper import group_by_speaker
from splitter import split_paragraphs
from markdown_formatter import generate_markdown
from utils import extract_date_from_filename, save_output

def process_transcript(file_path):
    raw_lines = clean_input(file_path)
    speaker_blocks = group_by_speaker(raw_lines)
    refined_blocks = [(s, split_paragraphs(t)) for s, t in speaker_blocks]
    date = extract_date_from_filename(file_path)
    md = generate_markdown(date, refined_blocks)
    save_output(file_path, md)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py transcript.txt")
    else:
        process_transcript(sys.argv[1])
