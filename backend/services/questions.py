"""Questionnaire: 47 questions in 10 categories. Users answer about SETTINGS/BEHAVIOUR only - never real phone/email/address."""
from collections import namedtuple
Q = namedtuple("Q", "id cat text kind rec")
# category key: (letter, name, default weight %)
CATEGORIES = {
 "profile": ("A", "Profile Visibility", 10), "personal": ("B", "Personal Information", 15),
 "location": ("C", "Location Privacy", 15), "content": ("D", "Posts & Content", 10),
 "connections": ("E", "Friends / Followers", 10), "tagging": ("F", "Tagging & Mentions", 5),
 "account": ("G", "Authentication & Account Security", 15), "apps": ("H", "Third-Party Apps", 5),
 "social_eng": ("I", "Messaging & Social Engineering", 10), "footprint": ("J", "Digital Footprint", 5)}
# kind: vis = PUBLIC/FRIENDS/PRIVATE | bad = YES is risky | good = YES is protective
OPTIONS = {"vis": ["PUBLIC", "FRIENDS", "PRIVATE", "NOT_SURE"],
           "bad": ["YES", "SOMETIMES", "NO", "NOT_SURE"], "good": ["YES", "SOMETIMES", "NO", "NOT_SURE"]}
RISK = {"vis": {"PUBLIC": 1, "FRIENDS": .4, "PRIVATE": 0, "NOT_SURE": .6},
        "bad": {"YES": 1, "SOMETIMES": .5, "NO": 0, "NOT_SURE": .6},
        "good": {"YES": 0, "SOMETIMES": .5, "NO": 1, "NOT_SURE": .7}}
BEST = {"vis": "PRIVATE", "bad": "NO", "good": "YES"}
WORST = {"vis": "PUBLIC", "bad": "YES", "good": "NO"}
QUESTIONS = [
 Q("a1","profile","Who can see your profile?","vis","Set your profile to Friends/Private unless you truly need it public."),
 Q("a2","profile","Can search engines show your profile in results?","bad","Turn off search-engine indexing of your profile."),
 Q("a3","profile","Who can see your friends/followers list?","vis","Limit friends/followers list visibility to Friends or Only me."),
 Q("a4","profile","Can strangers find you by phone number or email lookup?","bad","Disable discoverability by phone/email lookup."),
 Q("b1","personal","Who can see your phone number?","vis","Make your phone number private."),
 Q("b2","personal","Who can see your personal email?","vis","Hide your personal email; use a contact form or masked address."),
 Q("b3","personal","Who can see your full birth date (day, month, year)?","vis","Hide birth year, or the full birthday, from the public."),
 Q("b4","personal","Who can see your workplace?","vis","Restrict workplace details to connections you trust."),
 Q("b5","personal","Who can see your school/college?","vis","Restrict education details to trusted connections."),
 Q("b6","personal","Who can see family or relationship details?","vis","Hide family/relationship details from the public."),
 Q("b7","personal","Who can see your hometown or home area?","vis","Remove or restrict home-area information."),
 Q("c1","location","Do you share your real-time location publicly?","bad","Avoid broadcasting real-time location publicly."),
 Q("c2","location","Is geotagging enabled on your posts or photos?","bad","Turn off geotagging by default."),
 Q("c3","location","Do you publicly check in at places you visit?","bad","Stop public check-ins, or post after you have left."),
 Q("c4","location","Do you post travel plans before or during a trip?","bad","Share trip photos after you return."),
 Q("c5","location","Could someone work out your home or work location from your posts?","bad","Review posts for home/work clues and remove them."),
 Q("d1","content","Who can see your posts by default?","vis","Set default post audience to Friends."),
 Q("d2","content","Have you posted photos showing badges, documents, screens or number plates?","bad","Remove such posts; check backgrounds before posting."),
 Q("d3","content","Do you publicly post photos of children?","bad","Avoid public photos of children, or limit the audience."),
 Q("d4","content","Do you strip photo metadata (EXIF) before posting?","good","Remove EXIF metadata before sharing photos."),
 Q("e1","connections","Do you accept connection requests from unknown people?","bad","Verify unfamiliar profiles before accepting."),
 Q("e2","connections","Do you verify unfamiliar profiles before accepting them?","good","Check mutual friends, history and profile age before accepting."),
 Q("e3","connections","Do you periodically review your friends/followers?","good","Review and remove unknown connections every few months."),
 Q("e4","connections","Who can send you direct messages?","vis","Limit DMs to friends or people you follow."),
 Q("f1","tagging","Can anyone tag you without approval?","bad","Restrict who can tag you."),
 Q("f2","tagging","Is tag review enabled?","good","Enable tag review so you approve tags first."),
 Q("f3","tagging","Do tagged posts appear on your profile automatically?","bad","Require approval before tagged posts appear on your profile."),
 Q("f4","tagging","Can people you do not know mention you?","bad","Limit mentions to people you know."),
 Q("g1","account","Do you use multi-factor authentication (MFA)?","good","Enable MFA with the strongest method supported (app/security key)."),
 Q("g2","account","Is your password unique to this account?","good","Use a unique password for every account."),
 Q("g3","account","Do you use a password manager?","good","Adopt a reputable password manager."),
 Q("g4","account","Are login alerts enabled?","good","Enable login alerts."),
 Q("g5","account","Have you reviewed recovery email/phone recently?","good","Review account recovery options."),
 Q("g6","account","Do you review active sessions and devices?","good","Log out unknown sessions and devices."),
 Q("h1","apps","Do you regularly review connected third-party apps?","good","Review connected apps and revoke what you do not need."),
 Q("h2","apps","Do you have old or unused apps still connected?","bad","Remove unused integrations."),
 Q("h3","apps","Do you grant apps broad permissions without reading them?","bad","Apply least privilege: grant only needed permissions."),
 Q("h4","apps","Do you use 'Sign in with social account' on many sites?","bad","Prefer separate logins for low-trust sites."),
 Q("i1","social_eng","Do you reply to suspicious or unexpected DMs?","bad","Do not reply; report and block suspicious senders."),
 Q("i2","social_eng","Do you click unexpected links in messages?","bad","Do not click unexpected links; verify via another channel."),
 Q("i3","social_eng","Have you ever shared a verification code with someone?","bad","Never share verification codes with anyone."),
 Q("i4","social_eng","Do you verify messages that may come from impersonated accounts?","good","Confirm unusual requests with the person on another channel."),
 Q("i5","social_eng","Do you take part in unverified giveaways or prize offers?","bad","Avoid unverified giveaways; they are common scam vehicles."),
 Q("j1","footprint","Do you regularly review old public posts?","good","Review and remove or restrict old posts."),
 Q("j2","footprint","Do you have old or unused accounts still online?","bad","Delete unused accounts."),
 Q("j3","footprint","Do you review privacy settings periodically?","good","Schedule a privacy settings review every 3-6 months."),
 Q("j4","footprint","Do your public comments reveal personal details?","bad","Avoid personal details in public comments."),
]
QBY = {q.id: q for q in QUESTIONS}
