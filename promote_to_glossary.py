import json
from glossary_stats import load_stats
from collections import OrderedDict

def load_glossary(filepath="glossary.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_glossary(glossary, filepath="glossary.json"):
    sorted_glossary = OrderedDict(sorted(glossary.items()))
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sorted_glossary, f, indent=2)

def promote():
    stats = load_stats()
    glossary = load_glossary()

    print("📚 Promote unknown acronyms to glossary:
")
    for term, count in stats.most_common():
        if term in glossary:
            continue
        ans = input(f"[{count}] {term} → promote to glossary? [y/N]: ").strip().lower()
        if ans == "y":
            repl = input(f"    Enter replacement for '{term}': ").strip()
            if repl:
                glossary[term] = repl

    save_glossary(glossary)
    print("✅ Glossary updated.")

if __name__ == "__main__":
    promote()
