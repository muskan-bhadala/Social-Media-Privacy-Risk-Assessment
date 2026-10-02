"""Personalised, prioritised recommendations + printable checklist."""
from .questions import QBY
PRIORITY = {"HIGH": "IMMEDIATE", "MEDIUM": "IMPORTANT", "LOW": "GOOD_PRACTICE"}
CHECKLIST = ["Review profile visibility", "Hide unnecessary contact information", "Review birth-date visibility",
 "Review location sharing", "Avoid unnecessary real-time location posts", "Review tagging permissions",
 "Review followers/friends", "Verify unfamiliar requests", "Enable MFA", "Enable login alerts where available",
 "Review active sessions", "Review connected apps", "Remove unused integrations", "Review old public posts",
 "Review photo privacy", "Be cautious with unexpected links", "Never share verification codes",
 "Review privacy settings periodically"]

def generate_recommendations(findings):
    return [{"finding_type": f["finding_type"], "recommendation": QBY[f["finding_type"]].rec,
             "priority": PRIORITY[f["severity"]]} for f in findings]
