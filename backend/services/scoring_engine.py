"""Feature extraction + category scoring + overall risk. Higher = more exposure."""
from .questions import QUESTIONS, CATEGORIES, RISK

DEFAULT_WEIGHTS = {k: v[2] for k, v in CATEGORIES.items()}  # configurable; must sum to 100

def extract_privacy_features(answers):
    """Map each answer to a 0..1 risk contribution: {question_id: risk}."""
    return {q.id: RISK[q.kind][answers[q.id]] for q in QUESTIONS}

def category_scores(features):
    """Each category 0-100 = average risk of its questions."""
    out = {}
    for cat in CATEGORIES:
        vals = [features[q.id] for q in QUESTIONS if q.cat == cat]
        out[cat] = round(100 * sum(vals) / len(vals), 1)
    return out

def classify(score):
    """0-20 LOW, 21-40 MODERATE, 41-70 HIGH, 71-100 CRITICAL (educational thresholds)."""
    return "LOW" if score <= 20 else "MODERATE" if score <= 40 else "HIGH" if score <= 70 else "CRITICAL"

def calculate_privacy_risk(answers, weights=None):
    """Weighted overall score. Weights/thresholds are educational assumptions - validate before real decisions."""
    w = weights or DEFAULT_WEIGHTS
    if abs(sum(w.values()) - 100) > 1e-6 or set(w) != set(CATEGORIES):
        raise ValueError("weights must cover all categories and sum to 100")
    feats = extract_privacy_features(answers)
    cs = category_scores(feats)
    overall = round(sum(cs[c] * w[c] for c in cs) / 100)
    return {"overall_score": overall, "risk_level": classify(overall), "category_scores": cs, "features": feats}
