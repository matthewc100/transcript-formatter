# summarizer.py
# Routes summary and action item extraction to modular detectors

from summary_extractor import extract_summary
from action_extractor import extract_action_items as extract_actions

def generate_summary(blocks):
    return extract_summary(blocks)

def extract_action_items(blocks, debug=False):  # ← Add debug parameter here
    return extract_actions(blocks, debug=debug)  # ← Pass it through
