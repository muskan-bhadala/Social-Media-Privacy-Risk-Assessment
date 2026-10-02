import os, sqlite3, pytest
from services.questions import QUESTIONS, BEST, WORST, QBY
from services.scoring_engine import calculate_privacy_risk, classify, category_scores, extract_privacy_features, DEFAULT_WEIGHTS
from services.findings_engine import generate_privacy_findings
from services.assessment_engine import validate_answers, run_assessment
from services.improvement_simulator import simulate
from utils import db, report
from app import app

def safe(): return {q.id: BEST[q.kind] for q in QUESTIONS}
def risky(): return {q.id: WORST[q.kind] for q in QUESTIONS}
def flip(*ids):
    a = safe()
    for i in ids: a[i] = WORST[QBY[i].kind]
    return a
ACCT = ["g1", "g2", "g3", "g4", "g5", "g6"]

def test_question_count(): assert len(QUESTIONS) >= 40
def test_fully_private():
    r = calculate_privacy_risk(safe()); assert r["overall_score"] == 0 and r["risk_level"] == "LOW"
def test_fully_public():
    r = calculate_privacy_risk(risky()); assert r["overall_score"] == 100 and r["risk_level"] == "CRITICAL"

# phone, email, birthday, location, check-ins, travel, work, edu, posts, unknown conns, tag review, MFA, alerts, pw reuse, apps, links, old posts, settings review
@pytest.mark.parametrize("qid", ["b1","b2","b3","c1","c3","c4","b4","b5","d1","e1","f2","g1","g4","g2","h1","i2","j1","j3"])
def test_single_risk_detected(qid):
    r = calculate_privacy_risk(flip(qid)); assert r["overall_score"] > 0
    assert qid in [f["finding_type"] for f in generate_privacy_findings(r["features"])]

@pytest.mark.parametrize("score,level", [(0,"LOW"),(20,"LOW"),(21,"MODERATE"),(40,"MODERATE"),(41,"HIGH"),(70,"HIGH"),(71,"CRITICAL"),(100,"CRITICAL")])
def test_boundaries(score, level): assert classify(score) == level

def test_category_scores():
    cs = category_scores(extract_privacy_features(flip(*ACCT))); assert cs["account"] == 100 and cs["location"] == 0
def test_weights_validation():
    with pytest.raises(ValueError): calculate_privacy_risk(safe(), {"profile": 100})
def test_custom_weights():
    w = {k: 0 for k in DEFAULT_WEIGHTS}; w["account"] = 100
    assert calculate_privacy_risk(flip(*ACCT), w)["overall_score"] == 100
def test_validation_missing():
    with pytest.raises(ValueError): validate_answers({"a1": "PUBLIC"})
def test_validation_bad_value():
    a = safe(); a["g1"] = "<script>"
    with pytest.raises(ValueError): validate_answers(a)
def test_recommendations_priority():
    r = run_assessment(risky()); assert {x["priority"] for x in r["recommendations"]} <= {"IMMEDIATE","IMPORTANT","GOOD_PRACTICE"} and r["recommendations"]
def test_simulation():
    s = simulate(risky(), [q.id for q in QUESTIONS]); assert s["after"]["score"] == 0 and s["risk_reduction"] == 100
def test_simulation_unknown_id():
    with pytest.raises(ValueError): simulate(safe(), ["zzz"])
def test_db_save_and_no_sensitive_data():
    aid = db.save(run_assessment(risky())); assert db.get(aid)["risk_level"] == "CRITICAL"
    c = sqlite3.connect(os.environ["DB_PATH"])
    cols = {r[1] for t in ("assessments","category_scores","findings","recommendations") for r in c.execute(f"PRAGMA table_info({t})")}
    assert not cols & {"phone","email","address","birth_date","password","location","messages","answers"}
def test_report_generation():
    aid = db.save(run_assessment(risky())); html = report.build(db.get(aid)); assert "Disclaimer" in html and aid in html
def test_report_escapes():
    a = db.get(db.save(run_assessment(risky()))); a["findings"][0]["description"] = "<script>x</script>"
    assert "<script>x" not in report.build(a)
def test_api_flow():
    c = app.test_client(); ans = risky()
    r = c.post("/api/assessment", json={"answers": ans}); assert r.status_code == 201; aid = r.json["assessment_id"]
    assert c.get(f"/api/assessment/{aid}").status_code == 200
    assert c.get(f"/api/assessment/{aid}/recommendations").json["recommendations"]
    assert c.get(f"/api/assessment/{aid}/report").status_code == 200
    assert c.post("/api/assessment/simulate-improvement", json={"answers": ans, "fixes": ["g1"]}).json["risk_reduction"] > 0
    assert len(c.get("/api/privacy-checklist").json["checklist"]) >= 18
    assert "profiles" in c.get("/api/dashboard/stats").json
    assert c.delete(f"/api/assessment/{aid}").status_code == 200 and c.get(f"/api/assessment/{aid}").status_code == 404
def test_api_rejects_bad_input():
    c = app.test_client(); assert c.post("/api/assessment", json={"answers": {"a1": "x"}}).status_code == 400
    assert c.post("/api/assessment", data="notjson").status_code == 400
def test_security_headers():
    assert "Content-Security-Policy" in app.test_client().get("/api/privacy-checklist").headers
