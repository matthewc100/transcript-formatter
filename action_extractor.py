# action_extractor.py
# Modular action item detector with rule tiers, confidence levels, and optional debug logging

HARD_KEYWORDS = [
    "follow up", "confirm", "send", "reach out", "get back", "ask about",
    "circle back", "make sure", "i'll", "we'll", "can you", "need to"
]

SOFT_KEYWORDS = [
    "talk soon", "we'll talk", "we'll bug", "check in", "catch up", "see what happens"
]

def rule_matcher(line, debug=False):
    lowered = line.lower()
    for kw in HARD_KEYWORDS:
        if kw in lowered:
            if debug:
                print(f"[RULE HIGH] Matched hard keyword: '{kw}' in: {line}")
            return True, "rule_matcher [HIGH]", f"Matched hard keyword: {kw}"
    for kw in SOFT_KEYWORDS:
        if kw in lowered:
            if debug:
                print(f"[RULE LOW] Matched soft keyword: '{kw}' in: {line}")
            return True, "rule_matcher [LOW]", f"Matched soft keyword: {kw}"
    return False, "", ""

# Stub for NLP-based detection
def spacy_matcher(line, debug=False):
    return False, "", ""

def extract_action_items(blocks, debug=False):
    actions = []

    for speaker, paragraphs in blocks:
        for line in paragraphs:
            for matcher in [rule_matcher, spacy_matcher]:
                matched, source, reason = matcher(line, debug=debug)
                if matched:
                    actions.append({
                        "speaker": speaker,
                        "text": line,
                        "source": source,
                        "reason": reason
                    })
                    break  # Only one method flags each line
    return actions