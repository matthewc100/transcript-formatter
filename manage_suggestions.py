import json
from collections import OrderedDict
from glossary_stats import load_stats

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} if path.endswith(".json") else []

def save_json(data, path):
    if isinstance(data, dict):
        data = OrderedDict(sorted(data.items()))
    elif isinstance(data, list):
        data = sorted(set(data))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def manage():
    glossary = load_json("glossary.json")
    ignore_list = set(load_json("ignore_acronyms.json"))
    stats = load_stats()

    print("📚 Manage glossary and ignore list suggestions:")
    for term, count in stats.most_common():
        if term in glossary or term in ignore_list:
            continue

        print(f"[{count}] {term} → What do you want to do?")
        print("[p] Promote to glossary")
        print("[i] Ignore in future")
        print("[s] Skip for now")
        choice = input("> ").strip().lower()

        if choice == "p":
            repl = input(f"    Enter replacement for '{term}': ").strip()
            if repl:
                glossary[term] = repl
                print(f"✅ Added '{term}' → '{repl}' to glossary.")
        elif choice == "i":
            ignore_list.add(term)
            print(f"✅ Added '{term}' to ignore list.")
        elif choice == "s" or choice == "":
            print("⏭ Skipped.")
        else:
            print("⚠️ Invalid choice. Skipped.")

    save_json(glossary, "glossary.json")
    save_json(list(ignore_list), "ignore_acronyms.json")
    print("\n✅ Glossary and ignore list updated.")

if __name__ == "__main__":
    manage()
