# -*- coding: utf-8 -*-
"""
Gộp các file review của 4 người thành 1 file duy nhất (có khử trùng).

Chạy:  python merge_reviews.py

- Gộp vietnam_reviews_w1.json..w4.json  ->  vietnam_reviews_all.json
- Gộp vietnam_reviews_vi_w1.json..w4.json -> vietnam_reviews_vi_all.json (nếu có)
"""

import glob
import json
import os


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def merge(pattern, out_file):
    files = sorted(glob.glob(pattern))
    if not files:
        return
    seen, merged = set(), []
    for fp in files:
        data = load(fp)
        for r in data:
            sig = (r.get("url"), r.get("reviewer_url"), r.get("title"),
                   r.get("visit_date"), (r.get("comment") or "")[:60])
            if sig in seen:
                continue
            seen.add(sig)
            merged.append(r)
        print(f"  + {os.path.basename(fp)}: {len(data)} review")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"=> {out_file}: {len(merged)} review (đã khử trùng)\n")


if __name__ == "__main__":
    print("Gộp review tiếng Anh:")
    merge("vietnam_reviews_w*.json", "vietnam_reviews_all.json")
    print("Gộp review tiếng Việt:")
    merge("vietnam_reviews_vi_w*.json", "vietnam_reviews_vi_all.json")
