"""Validation + orchestration of the full pipeline."""
from .questions import QUESTIONS, OPTIONS
from .scoring_engine import calculate_privacy_risk
from .findings_engine import generate_privacy_findings
from .recommendation_engine import generate_recommendations

def validate_answers(data):
    """Whitelist validation: every question answered, value must be an allowed option. Returns clean dict."""
    if not isinstance(data, dict):
        raise ValueError("answers must be an object")
    clean, errs = {}, []
    for q in QUESTIONS:
        v = data.get(q.id)
        v = v.strip().upper() if isinstance(v, str) else v
        if v not in OPTIONS[q.kind]:
            errs.append(q.id)
        else:
            clean[q.id] = v
    if errs:
        raise ValueError("missing/invalid answers: " + ", ".join(errs[:10]))
    return clean

def run_assessment(answers):
    r = calculate_privacy_risk(answers)
    f = generate_privacy_findings(r["features"])
    return {"overall_score": r["overall_score"], "risk_level": r["risk_level"],
            "category_scores": r["category_scores"], "findings": f, "recommendations": generate_recommendations(f)}
