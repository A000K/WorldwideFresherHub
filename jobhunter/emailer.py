import os
import smtplib
from email.message import EmailMessage

def send_digest(jobs):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("ALERT_TO")
    if not all([sender, password, recipient]):
        print("Email not configured; skipping Gmail digest.")
        return

    msg = EmailMessage()
    msg["Subject"] = f"Global Fresher Job Hunter: {len(jobs)} new matches"
    msg["From"] = sender
    msg["To"] = recipient
    lines = ["New job matches (review eligibility and work authorisation):", ""]
    for job, score, reasons in jobs[:50]:
        lines += [
            f"{job['title']} — {job['company']}",
            f"Location: {job['location'] or 'Not specified'} | Match: {score}/100",
            f"Source: {job['source']}",
            f"Why matched: {', '.join(reasons)}",
            f"Apply: {job['url']}", ""
        ]
    msg.set_content("\n".join(lines))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
