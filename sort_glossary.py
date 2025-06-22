import json

def sort_glossary(filepath="glossary.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        glossary = json.load(f)

    sorted_glossary = dict(sorted(glossary.items()))

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sorted_glossary, f, indent=2)
        print(f"✅ Sorted glossary saved to {filepath}")

if __name__ == "__main__":
    sort_glossary()
