#!/usr/bin/env python3
# pipeline_controller.py
# Transcript processing pipeline with action item debug logging support

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

def process_pipeline(file_path, output_dir, use_summary, use_glossary, grammar_check, autofix_grammar, debug_actions):
    glossary = load_glossary() if use_glossary else {}
    ignore_set = load_ignored() if use_glossary else set()
    grammar_tool = get_grammar_tool() if grammar_check or autofix_grammar else None
    grammar_after = []
    unknowns = {}
    final_blocks = []

    raw_lines = clean_input(file_path)
    speaker_blocks = group_by_speaker(raw_lines)

    for speaker, turn in speaker_blocks:
        paragraphs = split_paragraphs(turn)
        cleaned = []

        for para in paragraphs:
            if autofix_grammar and grammar_tool:
                para = apply_auto_fixes(para, grammar_tool)

            if use_glossary:
                substituted, found = apply_substitutions(para, glossary, ignore_set, log_unknowns=True)
                para = substituted
                for term, ctxs in found.items():
                    unknowns.setdefault(term, []).extend(ctxs)

            if grammar_check and grammar_tool:
                issues = check_paragraph(para, grammar_tool)
                for issue in issues:
                    grammar_after.append(f"{speaker}: {issue['message']} | '{issue['context']}' → {', '.join(issue['suggestions'])}")

            cleaned.append(para)

        final_blocks.append((speaker, cleaned))

    date = extract_date_from_filename(file_path)
    summary, actions = (None, [])
    if use_summary:
        summary = generate_summary(final_blocks)
        actions = extract_action_items(final_blocks, debug=debug_actions)

    out_path = Path(output_dir) / (Path(file_path).stem + ".formatted.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(generate_markdown(date, final_blocks, summary, actions))

    if use_glossary and unknowns:
        with open("glossary_suggestions.txt", "a", encoding="utf-8") as f:
            for term, contexts in sorted(unknowns.items()):
                for ctx in contexts:
                    f.write(f'  - {term} → "{ctx.strip()}"\n')
        print("📄 Saved acronym review log to: glossary_suggestions.txt")

    if grammar_check and grammar_after:
        review_path = out_path.with_name(out_path.stem + "_grammar_review.txt")
        with open(review_path, "w", encoding="utf-8") as f:
            for line in grammar_after:
                f.write(line + "\n")
        print(f"📝 Saved grammar review log to: {review_path}")

    print(f"✅ Transcript saved to: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcript formatter pipeline")
    parser.add_argument("input_file", help="Path to the input .vtt or .txt transcript")
    parser.add_argument("--output-dir", default=".", help="Directory to save formatted Markdown and logs")
    parser.add_argument("--with-summary", action="store_true", help="Include summary and action items")
    parser.add_argument("--grammar-check", action="store_true", help="Enable grammar checking (after autofix)")
    parser.add_argument("--autofix-grammar", action="store_true", help="Automatically fix safe grammar issues")
    parser.add_argument("--substitute-glossary", action="store_true", help="Enable glossary-based substitutions")
    parser.add_argument("--debug-actions", action="store_true", help="Print diagnostic output for action extraction")
    args = parser.parse_args()

    process_pipeline(
        file_path=args.input_file,
        output_dir=args.output_dir,
        use_summary=args.with_summary,
        use_glossary=args.substitute_glossary,
        grammar_check=args.grammar_check,
        autofix_grammar=args.autofix_grammar,
        debug_actions=args.debug_actions
    )