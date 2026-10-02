"""Flask app: REST API + static frontend. Run: python backend/app.py"""
import os, sys, csv, time, collections
sys.path.insert(0, os.path.dirname(__file__))
from flask import Flask, jsonify, request, Response
from services.questions import QUESTIONS, CATEGORIES, OPTIONS, QBY
from services.assessment_engine import validate_answers, run_assessment
from services.improvement_simulator import simulate
from services.recommendation_engine import CHECKLIST, generate_recommendations
from services.scoring_engine import extract_privacy_features, category_scores
from utils import db, report

ROOT = os.path.join(os.path.dirname(__file__), "..")
app = Flask(__name__, static_folder=os.path.join(ROOT, "frontend"), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = 20_000  # tiny payloads only
_hits = collections.defaultdict(list)

@app.before_request
def rate_limit():  # simple in-memory limiter per IP (per minute)
    if request.path.startswith("/api/"):
        lim, now = int(os.getenv("RATE_LIMIT", "60")), time.time()
        h = _hits[request.remote_addr] = [t for t in _hits[request.remote_addr] if now - t < 60]
        if len(h) >= lim: return jsonify(error="rate limit exceeded"), 429
        h.append(now)

@app.after_request
def headers(r):
    r.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'"
    r.headers["X-Content-Type-Options"] = "nosniff"; r.headers["Referrer-Policy"] = "no-referrer"
    return r

@app.errorhandler(413)
def too_big(_): return jsonify(error="payload too large"), 413

@app.errorhandler(ValueError)
def bad(e): return jsonify(error=str(e)), 400

def body():
    d = request.get_json(silent=True)
    if not isinstance(d, dict): raise ValueError("JSON object body required")
    return d

@app.get("/")
def home(): return app.send_static_file("index.html")

@app.get("/api/questions")
def questions():
    return jsonify(questions=[{"id": q.id, "text": q.text, "options": OPTIONS[q.kind], "category": q.cat,
        "letter": CATEGORIES[q.cat][0], "category_name": CATEGORIES[q.cat][1]} for q in QUESTIONS],
        categories={k: v[1] for k, v in CATEGORIES.items()})

@app.post("/api/assessment")
def create():
    res = run_assessment(validate_answers(body().get("answers")))  # answers are NOT stored
    res["assessment_id"] = db.save(res)
    for f in res["findings"]: f.pop("points", None)
    return jsonify(res), 201

@app.get("/api/assessment/<aid>")
def get_one(aid):
    a = db.get(aid); return (jsonify(a), 200) if a else (jsonify(error="not found"), 404)

@app.get("/api/assessment/<aid>/recommendations")
def recs(aid):
    a = db.get(aid)
    if not a: return jsonify(error="not found"), 404
    return jsonify(recommendations=generate_recommendations(a["findings"]))

@app.get("/api/assessment/<aid>/report")
def rep(aid):
    a = db.get(aid)
    return Response(report.build(a), mimetype="text/html") if a else (jsonify(error="not found"), 404)

@app.delete("/api/assessment/<aid>")
def delete(aid): return (jsonify(deleted=True), 200) if db.delete(aid) else (jsonify(error="not found"), 404)

@app.post("/api/assessment/simulate-improvement")
def sim():
    d = body(); fixes = d.get("fixes", [])
    if not isinstance(fixes, list): raise ValueError("fixes must be a list")
    return jsonify(simulate(validate_answers(d.get("answers")), fixes))

@app.get("/api/privacy-checklist")
def checklist(): return jsonify(checklist=CHECKLIST)

_cache = {}
def dataset_stats():
    if "s" in _cache: return _cache["s"]
    path = os.path.join(ROOT, "data", "social_media_privacy_assessments.csv")
    n, tot, dist = 0, 0, collections.Counter(); cats = collections.Counter(); weak = collections.Counter()
    if os.path.exists(path):
        for row in csv.DictReader(open(path, encoding="utf-8")):
            n += 1; tot += int(row["risk_score"]); dist[row["risk_level"]] += 1
            f = extract_privacy_features(row)
            for k, v in category_scores(f).items(): cats[k] += v
            for q, r in f.items():
                if r >= .5: weak[q] += 1
    top = [{"finding_type": q, "text": QBY[q].text, "percent": round(100 * c / n, 1)} for q, c in weak.most_common(8)] if n else []
    ctl = {"MFA": "g1", "Login alerts": "g4", "Unique password": "g2", "Password manager": "g3", "Tag review": "f2", "App review": "h1"}
    controls = {k: round(100 - 100 * weak[v] / n, 1) for k, v in ctl.items()} if n else {}
    _cache["s"] = {"profiles": n, "avg_score": round(tot / n, 1) if n else 0,
        "distribution": {k: dist.get(k, 0) for k in ("LOW", "MODERATE", "HIGH", "CRITICAL")},
        "category_avg": {CATEGORIES[k][1]: round(v / n, 1) for k, v in cats.items()} if n else {},
        "top_weaknesses": top, "controls_enabled_pct": controls, "synthetic": True}
    return _cache["s"]

@app.get("/api/dashboard/stats")
def stats(): return jsonify({**dataset_stats(), **db.aggregate()})

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "5000")), debug=False)
