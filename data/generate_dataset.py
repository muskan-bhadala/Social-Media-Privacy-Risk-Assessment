"""Generate 1,000 FICTIONAL privacy assessments. Run: python data/generate_dataset.py"""
import os, sys, csv, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "backend"))
from services.questions import QUESTIONS, BEST, WORST
from services.scoring_engine import calculate_privacy_risk
random.seed(42)
rows = []
for i in range(1, 1001):
    careless = random.betavariate(2, 2)  # fictional persona carelessness 0..1
    ans = {}
    for q in QUESTIONS:
        x = random.random()
        if x < careless * 0.8: ans[q.id] = WORST[q.kind]
        elif x < careless * 0.8 + 0.15: ans[q.id] = "FRIENDS" if q.kind == "vis" else "SOMETIMES"
        else: ans[q.id] = BEST[q.kind]
    r = calculate_privacy_risk(ans)
    rows.append({"profile_id": f"SYN-{i:04d}", **ans, "risk_score": r["overall_score"], "risk_level": r["risk_level"]})
out = os.path.join(HERE, "social_media_privacy_assessments.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("Wrote", out, len(rows), "synthetic rows")
