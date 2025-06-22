#!/usr/bin/env python3
# =============================================================================
# pipeline_controller.py
# -----------------------------------------------------------------------------
# Transcript Formatter Pipeline Controller
#
# This is the primary CLI entry point for processing transcripts. It orchestrates
# a multi-stage pipeline that:
#   - Cleans and parses transcript files (.vtt or .txt)
#   - Groups text by speaker
#   - Splits text into paragraphs
#   - Applies glossary-based substitutions
#   - Optionally performs grammar checking and correction
#   - Optionally extracts summary and action items
#   - Outputs a clean, structured Markdown file and optional review logs
# =============================================================================

import argparse
from substituter import load_glossary, load_ignored, apply_substitutions
from grammar_check import get_grammar_tool, check_paragraph, apply_auto_fixes
from utils import extract_date_from_filename
from summarizer import generate_summary, extract_action_items
from markdown_formatter import generate_markdown
from parser import clean_input
from grouper import group_by_speaker
from splitter import split_paragraphs
from pathlib import Path

def process_pipeline(file_path, output_dir, use_summary, use_glossary, enable_grammar):
    # === Setup: Load glossary and grammar tools ===
    glossary = load_glossary() if use_glossary else {}
    ignore_set = load_ignored() if use_glossary else set()
    grammar_tool = get_grammar_tool() if enable_grammar else None
    grammar_after = []  # To store grammar issues for logging
    unknowns = {}       # To collect unknown glossary tokens
    final_blocks = []   # To store structured speaker+paragraph output

    # === Phase 1: Clean raw transcript lines ===
    raw_lines = clean_input(file_path)  # Remove timestamps, normalize
    speaker_blocks = group_by_speaker(raw_lines)  # Aggregate lines by speaker

    # === Phase 2: Split speaker blocks into paragraphs ===
    for speaker, turn in speaker_blocks:
        paragraphs = split_paragraphs(turn)  # Sentence segmentation
        cleaned = []

        for para in paragraphs:
            # === Phase 3: Auto-fix known grammar issues (e.g. spacing) ===
            para = apply_auto_fixes(para, grammar_tool) if enable_grammar else para

            # === Phase 4: Glossary substitution and acronym detection ===
            if use_glossary:
                substituted, found = apply_substitutions(para, glossary, ignore_set, log_unknowns=True)
                para = substituted
                for term, ctxs in found.items():
                    unknowns.setdefault(term, []).extend(ctxs)

            # === Phase 5: Optional grammar check after all fixes ===
            if enable_grammar:
                print('[GRAMMAR CHECK] Checking cleaned paragraph:', para)
                issues = check_paragraph(para, grammar_tool)
                print(f"[GRAMMAR FOUND] {len(issues)} issues for: {speaker}")
                for issue in issues:
                    grammar_after.append(f"{speaker}: {issue['message']} | '{issue['context']}' → {', '.join(issue['suggestions'])}")

            # Collect cleaned paragraph
            cleaned.append(para)

        # Store speaker-paragraph pair
        final_blocks.append((speaker, cleaned))

    # === Phase 6: Optional summary generation ===
    date = extract_date_from_filename(file_path)
    summary, actions = (None, [])
    if use_summary:
        summary = generate_summary(final_blocks)
        actions = extract_action_items(final_blocks)

    # === Phase 7: Generate final Markdown output ===
    out_path = Path(output_dir) / (Path(file_path).stem + ".formatted.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(generate_markdown(date, final_blocks, summary, actions))

    # === Phase 8: Save glossary suggestions, if any ===
    if use_glossary and unknowns:
        with open("glossary_suggestions.txt", "a", encoding="utf-8") as f:
            for term, contexts in sorted(unknowns.items()):
                for ctx in contexts:
                    f.write(f'  - {term} → "{ctx.strip()}"\n')
        print("📄 Saved acronym review log to: glossary_suggestions.txt")

    # === Phase 9: Save grammar review log, if issues were found ===
    if enable_grammar and grammar_after:
        review_path = out_path.with_name(out_path.stem + "_grammar_review.txt")
        with open(review_path, "w", encoding="utf-8") as f:
            for line in grammar_after:
                f.write(line + "\n")
        print(f"📝 Saved grammar review log to: {review_path}")

    # === Final status ===
    print(f"✅ Transcript saved to: {out_path}")

# === CLI Argument Parsing ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcript formatter pipeline")
    parser.add_argument("input_file", help="Path to the input .vtt or .txt transcript")
    parser.add_argument("--output-dir", default=".", help="Directory to save formatted Markdown and logs")
    parser.add_argument("--with-summary", action="store_true", help="Include summary and action items")
    parser.add_argument("--grammar-check", action="store_true", help="Enable grammar checking (after autofix)")
    parser.add_argument("--substitute-glossary", action="store_true", help="Enable glossary-based substitutions")
    args = parser.parse_args()

    # === Start the processing pipeline ===
    process_pipeline(
        file_path=args.input_file,
        output_dir=args.output_dir,
        use_summary=args.with_summary,
        use_glossary=args.substitute_glossary,
        enable_grammar=args.grammar_check
    )