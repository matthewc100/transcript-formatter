import json
import re
from collections import defaultdict, Counter
from glossary_stats import update_stats

def load_glossary(filepath="glossary.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_ignored(filepath="ignore_acronyms.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def extract_context(text, keyword, window=5):
    words = text.split()
    contexts = []
    for i, word in enumerate(words):
        if word.lower() == keyword.lower():
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            context = " ".join(words[start:end])
            contexts.append(context)
    return contexts

def apply_substitutions(text, glossary, ignore_set, log_unknowns=False):
    unknown_contexts = defaultdict(list)
    frequency = Counter()

    for wrong, correct in glossary.items():
        pattern = r'\b' + re.escape(wrong) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):
            text = re.sub(pattern, correct, text, flags=re.IGNORECASE)

    if log_unknowns:
        tokens = re.findall(r'\b[A-Z]{2,5}\b', text)
        for token in tokens:
            if token not in glossary.values() and token not in ignore_set:
                contexts = extract_context(text, token)
                if contexts:
                    unknown_contexts[token].extend(contexts)
                    frequency[token] += 1

        update_stats(frequency)

        with open("glossary_suggestions.txt", "a", encoding="utf-8") as f:
            for token, ctxs in unknown_contexts.items():
                for c in ctxs:
                    f.write(f"{token} → {c.strip()}\n")

    return text, unknown_contexts if log_unknowns else text
