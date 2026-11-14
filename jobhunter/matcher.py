import re
from html import unescape

def clean(text):
    text = unescape(re.sub(r"<[^>]+>", " ", text or ""))
    return re.sub(r"\s+", " ", text).lower()

def score_job(job, profile):
    title = clean(job.get("title"))
    body = clean(job.get("description"))
    location = clean(job.get("location"))
    full = f"{title} {body}"

    # Reject clear seniority mismatches; do not assume every role is eligible.
    senior_terms = ["senior", "staff engineer", "principal", "lead engineer",
                    "manager", "director", "10+ years", "5+ years"]
    if any(term in title for term in senior_terms):
        return 0, ["Likely senior role"]

    role_hits = [r for r in profile.get("roles", []) if clean(r) in title]
    skill_hits = [s for s in profile.get("skills", []) if clean(s) in full]
    early_terms = ["graduate", "new grad", "entry level", "entry-level",
                   "junior", "trainee", "fresher", "intern", "0-1 years",
                   "0-2 years", "no experience"]
    early_hit = any(term in full for term in early_terms)

    score = min(55, len(set(skill_hits)) * 7)
    score += min(30, len(set(role_hits)) * 15)
    score += 15 if early_hit else 0
    reasons = []
    if role_hits:
        reasons.append("Role match: " + ", ".join(role_hits[:5]))
    if skill_hits:
        reasons.append("Skill match: " + ", ".join(skill_hits[:10]))
    if early_hit:
        reasons.append("Contains graduate/entry-level wording")
    if not reasons:
        reasons.append("Weak keyword match; review manually")

    # Location is displayed for review. Work eligibility is never inferred.
    if not location:
        reasons.append("Location not specified; verify")
    return min(score, 100), reasons
