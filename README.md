# Social Media Privacy Risk Assessment Framework

Defensive, educational cybersecurity project. Users answer a 47-question self-assessment about their social-media settings and habits. The app returns a 0-100 risk score (higher = more exposure), category scores, findings, prioritised recommendations, an improvement simulator, a dashboard and a printable report.

> This project is designed for defensive cybersecurity and privacy education. It uses synthetic or voluntarily provided assessment responses and does not scrape, track, or profile real social-media users.

Educational framework only: it is not a guarantee that an account will or will not be compromised. Weights and thresholds are educational assumptions and need calibration before any professional use.

## Quick start (Windows: use `venv\Scripts\activate`)
```bash
cd Social-Media-Privacy-Risk-Assessment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python data/generate_dataset.py      # 1,000 synthetic profiles
python -m pytest -q                  # automated tests
python backend/app.py                # open http://127.0.0.1:5000
```
Then: Start Privacy Assessment -> answer (or click "Load fictional demo profile") -> Calculate -> view radar chart -> run the simulator -> open the report (browser Print -> Save as PDF) -> visit Dashboard.

## Scoring
Answer -> risk 0..1 -> category score 0-100 (mean) -> weighted overall (A 10, B 15, C 15, D 10, E 10, F 5, G 15, H 5, I 10, J 5). 0-20 LOW, 21-40 MODERATE, 41-70 HIGH, 71-100 CRITICAL. Weights are configurable in `scoring_engine.calculate_privacy_risk(answers, weights)`.

## Folders
- `backend/app.py` Flask app, REST API, rate limit, security headers
- `backend/services/` questions, scoring, findings, recommendations, simulator, validation
- `backend/utils/` SQLite storage (scores + finding types only) and HTML report
- `frontend/` index, assessment, dashboard pages (+ css/js; Chart.js via CDN)
- `data/` synthetic dataset generator + CSV
- `tests/` 43 pytest cases; `reports/ screenshots/ docs/` for your proof of work

## API
| Method | Path | Purpose |
|---|---|---|
| GET | /api/questions | questionnaire |
| POST | /api/assessment | `{"answers":{id:value}}` -> score (201) |
| GET | /api/assessment/{id} | stored scores/findings |
| GET | /api/assessment/{id}/recommendations | prioritised fixes |
| GET | /api/assessment/{id}/report | printable HTML report |
| POST | /api/assessment/simulate-improvement | `{"answers":{...},"fixes":["g1","b1"]}` |
| GET | /api/dashboard/stats | synthetic + live aggregates |
| GET | /api/privacy-checklist | checklist |
| DELETE | /api/assessment/{id} | delete stored assessment |

Errors: 400 invalid input, 404 not found, 413 too large, 429 rate limited. No accounts are implemented, so there is no authentication; add auth before any multi-user deployment.

## Privacy by design
Data minimisation: we ask "is it visible?", never for the value. Raw answers are never stored; DB holds scores, finding types and timestamp only. Purpose limitation: data is used only for scoring. Delete endpoint = user control. Whitelist input validation, escaped output, CSP header, request-size cap, rate limiting.

## Privacy vs security
Privacy controls what personal information is exposed; security protects accounts from unauthorised access. A strong password with public phone, birthday and location is good security but poor privacy.

## Limitations / future work
Self-reported answers; assumed weights; no platform-specific checklists. Future: calibration, platform checklists, quizzes, comparison over time, local-only mode, accessibility and localisation.

## GitHub
```bash
git init && git add . && git commit -m "Initialize social media privacy risk assessment"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```
Topics: cybersecurity privacy social-media-privacy privacy-risk security-awareness python flask digital-footprint risk-assessment grc privacy-by-design defensive-security
