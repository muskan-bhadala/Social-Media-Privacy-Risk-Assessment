"""'What if I improve my settings?' - framework simulation, NOT a guarantee of safety."""
from .questions import QBY, BEST
from .scoring_engine import calculate_privacy_risk

def simulate(answers, fixes):
    new = dict(answers)
    for qid in fixes:
        if qid not in QBY:
            raise ValueError("unknown question id: " + str(qid))
        new[qid] = BEST[QBY[qid].kind]
    b, a = calculate_privacy_risk(answers), calculate_privacy_risk(new)
    return {"before": {"score": b["overall_score"], "level": b["risk_level"], "categories": b["category_scores"]},
            "after": {"score": a["overall_score"], "level": a["risk_level"], "categories": a["category_scores"]},
            "risk_reduction": b["overall_score"] - a["overall_score"],
            "disclaimer": "Framework simulation only; not a guarantee of real-world safety."}
