"""Printable HTML report (browser Print -> Save as PDF). All values HTML-escaped; no sensitive data."""
from html import escape as e
from services.questions import CATEGORIES
from services.recommendation_engine import generate_recommendations, CHECKLIST

def build(a):
    recs = generate_recommendations(a["findings"])
    rows = "".join(f"<tr><td>{e(CATEGORIES[k][1])}</td><td>{float(v)}/100</td></tr>" for k, v in a["category_scores"].items())
    fl = "".join(f"<li><b>{e(f['severity'])}</b> - {e(f['description'])}</li>" for f in a["findings"][:10])
    rl = "".join(f"<li><b>{e(r['priority'])}</b>: {e(r['recommendation'])}</li>" for r in recs)
    cl = "".join(f"<li>&#9633; {e(c)}</li>" for c in CHECKLIST)
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Privacy Assessment {e(a['assessment_id'])}</title>
<style>body{{font-family:Georgia,serif;max-width:800px;margin:2rem auto;line-height:1.5}}td{{border-bottom:1px solid #ccc;padding:4px 12px}}ul{{list-style:none;padding:0}}</style></head><body>
<h1>Social Media Privacy Risk Assessment</h1>
<p>Assessment ID: {e(a['assessment_id'])}<br>Date: {e(a['created_at'])}</p>
<h2>Overall risk: {int(a['overall_score'])}/100 - {e(a['risk_level'])}</h2>
<h3>Category scores (higher = more exposure)</h3><table>{rows}</table>
<h3>Top findings</h3><ul>{fl}</ul><h3>Recommendations by priority</h3><ul>{rl}</ul>
<h3>Privacy checklist</h3><ul>{cl}</ul>
<h3>Disclaimer</h3><p>Educational risk framework based on self-reported answers. It is not a guarantee that an account will or will not be compromised. Weights and thresholds are educational assumptions. This report contains no personal data.</p>
</body></html>"""
