import json
from pathlib import Path
from collections import Counter

STATS_FILE = "acronym_stats.json"

def load_stats():
    if Path(STATS_FILE).exists():
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return Counter(json.load(f))
    return Counter()

def update_stats(stats_counter):
    current = load_stats()
    current.update(stats_counter)
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(dict(current.most_common()), f, indent=2)
