# main.py
# Transcript Formatter: Entry point for CLI
# Supports summary generation, glossary substitution, grammar checking, and optional auto-fixes.

import argparse
from parser import clean_input
from grouper import group_by_speaker
from splitter import split_paragraphs
from markdown_formatter import generate_markdown
from utils import extract_date_from_filename, save_output
from summarizer import generate_summary, extract_action_items
from substituter import load_glossary, load_ignored, apply_substitutions
from grammar_check import get_grammar_tool, check_paragraph, apply_auto_fixes
from pathlib import Path

def process_transcript(file_path, include_summary, use_glossary, output_dir, grammar_check, autofix_grammar):
    glossary = load_glossary() if use_glossary else {}
    ignore_set = load_ignored() if use_glossary else set()
    grammar_tool = get_grammar_tool() if grammar_check or autofix_grammar else None
    grammar_log = []

    raw_lines = clean_input(file_path)
    speaker_blocks = group_by_speaker(raw_lines)
    refined_blocks = []
    all_unknowns = {}

    for speaker, turn in speaker_blocks:
        paragraphs = split_paragraphs(turn)
        processed = []

        for para in paragraphs:
            if use_glossary:
                substituted, unknowns = apply_substitutions(para, glossary, ignore_set, log_unknowns=True)
                para = substituted
                for term, snippets in unknowns.items():
                    all_unknowns.setdefault(term, []).extend(snippets)

            if autofix_grammar and grammar_tool:
                para = apply_auto_fixes(para, grammar_tool)

            if grammar_check and grammar_tool:
                grammar_issues = check_paragraph(para, grammar_tool)
                for issue in grammar_issues:
                    msg = f"{speaker}: {issue['message']} | '{issue['context']}' → {', '.join(issue['suggestions'])}"
                    grammar_log.append(msg)
                    print(msg)

            processed.append(para)

        refined_blocks.append((speaker, processed))

    # Extract date from filename
    date = extract_date_from_filename(file_path)

    # Generate optional summary and action items
    summary, action_items = (None, [])
    if include_summary:
        summary = generate_summary(refined_blocks)
        action_items = extract_action_items(refined_blocks)

    # Save glossary suggestions
    if use_glossary and all_unknowns:
        print("🔎 Unknown acronyms or tokens worth reviewing:")
        with open("glossary_suggestions.txt", "a", encoding="utf-8") as logf:
            for term, contexts in sorted(all_unknowns.items()):
                for ctx in contexts:
                    msg = f'  - {term} → "{ctx.strip()}"'
                    print(msg)
                    logf.write(msg + "\n")
        print("📄 Saved acronym review log to: glossary_suggestions.txt")

    # Save formatted Markdown
    output_path = Path(output_dir) / (Path(file_path).stem + ".formatted.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        md = generate_markdown(date, refined_blocks, summary, action_items)
        f.write(md)
    print(f"✅ Saved transcript to: {output_path}")

    # Save grammar review log
    if grammar_check and grammar_log:
        grammar_file = output_path.with_name(output_path.stem + "_grammar_review.txt")
        with open(grammar_file, "w", encoding="utf-8") as gf:
            for entry in grammar_log:
                gf.write(entry + "\n")
        print(f"📝 Saved grammar review log to: {grammar_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a transcript file into structured Markdown.")
    parser.add_argument("input_file", help="Path to the transcript input file (.txt or .vtt)")
    parser.add_argument("--with-summary", action="store_true", help="Include a summary and action items")
    parser.add_argument("--debug-no-summary", action="store_true", help="Skip summary even if requested")
    parser.add_argument("--substitute-glossary", action="store_true", help="Apply glossary substitutions and detect acronyms")
    parser.add_argument("--grammar-check", action="store_true", help="Enable grammar validation and logging")
    parser.add_argument("--autofix-grammar", action="store_true", help="Automatically fix safe grammar issues (e.g., extra spaces)")
    parser.add_argument("--output-dir", default=".", help="Directory for output Markdown file")

    args = parser.parse_args()
    use_summary = args.with_summary and not args.debug_no_summary
    process_transcript(args.input_file, use_summary, args.substitute_glossary, args.output_dir, args.grammar_check, args.autofix_grammar)
