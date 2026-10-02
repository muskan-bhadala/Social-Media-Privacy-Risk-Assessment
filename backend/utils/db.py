"""Privacy-first SQLite storage: scores + finding types only. NO raw answers, contacts, locations, passwords."""
import os, sqlite3, uuid, datetime
DEFAULT = os.path.join(os.path.dirname(__file__), "..", "privacy.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS assessments(assessment_id TEXT PRIMARY KEY, overall_score INTEGER, risk_level TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS category_scores(category_score_id INTEGER PRIMARY KEY AUTOINCREMENT, assessment_id TEXT, category TEXT, score REAL);
CREATE TABLE IF NOT EXISTS findings(finding_id INTEGER PRIMARY KEY AUTOINCREMENT, assessment_id TEXT, category TEXT, finding_type TEXT, severity TEXT, description TEXT);
CREATE TABLE IF NOT EXISTS recommendations(recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT, finding_type TEXT, recommendation TEXT, priority TEXT);
"""
def conn():
    c = sqlite3.connect(os.getenv("DB_PATH", DEFAULT)); c.row_factory = sqlite3.Row
    c.executescript(SCHEMA); return c

def save(res):
    aid = uuid.uuid4().hex[:12]; c = conn()
    c.execute("INSERT INTO assessments VALUES(?,?,?,?)", (aid, res["overall_score"], res["risk_level"],
              datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")))
    c.executemany("INSERT INTO category_scores(assessment_id,category,score) VALUES(?,?,?)",
                  [(aid, k, v) for k, v in res["category_scores"].items()])
    c.executemany("INSERT INTO findings(assessment_id,category,finding_type,severity,description) VALUES(?,?,?,?,?)",
                  [(aid, f["category"], f["finding_type"], f["severity"], f["description"]) for f in res["findings"]])
    c.commit(); c.close(); return aid

def get(aid):
    c = conn(); a = c.execute("SELECT * FROM assessments WHERE assessment_id=?", (aid,)).fetchone()
    if not a: c.close(); return None
    out = dict(a)
    out["category_scores"] = {r["category"]: r["score"] for r in c.execute("SELECT * FROM category_scores WHERE assessment_id=?", (aid,))}
    out["findings"] = [dict(r) for r in c.execute("SELECT finding_type,category,severity,description FROM findings WHERE assessment_id=? ORDER BY finding_id", (aid,))]
    c.close(); return out

def delete(aid):
    c = conn(); n = 0
    for t in ("category_scores", "findings", "assessments"):
        n = c.execute(f"DELETE FROM {t} WHERE assessment_id=?", (aid,)).rowcount
    c.commit(); c.close(); return n > 0

def aggregate():
    c = conn(); r = c.execute("SELECT COUNT(*) n, AVG(overall_score) a FROM assessments").fetchone(); c.close()
    return {"user_assessments": r["n"], "user_avg_score": round(r["a"] or 0, 1)}
