"""Turns risky features into ranked findings."""
from .questions import QUESTIONS, CATEGORIES

def generate_privacy_findings(features):
    out = []
    for q in QUESTIONS:
        r = features[q.id]
        if r < 0.5:
            continue  # only moderately/highly risky answers become findings
        n = sum(1 for x in QUESTIONS if x.cat == q.cat)
        pts = r * CATEGORIES[q.cat][2] / n  # points this answer adds to the overall score
        sev = "HIGH" if pts >= 3 else "MEDIUM" if pts >= 1.5 else "LOW"
        out.append({"finding_type": q.id, "category": q.cat, "severity": sev,
                    "description": "Self-reported risk: " + q.text, "points": round(pts, 2)})
    return sorted(out, key=lambda f: -f["points"])
