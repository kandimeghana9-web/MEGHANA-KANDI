import csv
import json
from pathlib import Path


def load_payload(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_items(items):
    return sorted(items, key=lambda x: (-float(x.get("weight", 0)), x.get("title", "")))


def export_top_n(input_path: str | Path, output_path: str | Path, limit: int = 5):
    payload = load_payload(input_path)
    items = sort_items(payload.get("items", []))[:limit]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "id",
            "title",
            "category",
            "weight",
            "difficulty",
            "confidence",
            "reason",
            "anti_hype_score",
            "tags",
            "url",
            "timestamp",
        ])
        for item in items:
            writer.writerow([
                item.get("id", ""),
                item.get("title", ""),
                item.get("category", ""),
                item.get("weight", ""),
                item.get("difficulty", ""),
                item.get("confidence", ""),
                item.get("reason", ""),
                item.get("anti_hype_score", ""),
                "; ".join(item.get("tags", [])),
                item.get("url", ""),
                item.get("timestamp", ""),
            ])

    return items


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    payload_path = base / "recommendations.json"
    output_path = base / "recommendations_top5.csv"
    top_items = export_top_n(payload_path, output_path, limit=5)
    print(f"Exported {len(top_items)} top recommendations to {output_path.name}")
    for item in top_items:
        print(f"{item['weight']}: {item['title']} ({item['category']})")
