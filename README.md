# Global Fresher Job Hunter

A GitHub Actions-based starter project for discovering entry-level jobs worldwide,
matching them against a CSIT fresher profile, tracking applications, and sending
email digests.

## Important status

This starter **discovers and matches jobs** from public Greenhouse and Lever job
board feeds. It does **not** blindly submit applications to arbitrary websites.
Real application submission requires a site-specific adapter, the candidate's
verified answers, and compliance with each employer's terms. CAPTCHA, OTP,
assessments, legal declarations, work-authorisation questions, and other
attestations are handed to the candidate.

Never put passwords, OTPs, session cookies, or API keys in the repository.

## Included

- Daily GitHub Actions workflow
- Greenhouse and Lever public job-board discovery
- Resume-keyword matching and freshness/entry-level filtering
- SQLite application/job tracker (CSV export)
- Optional Gmail SMTP digest
- Profile stored separately in `config/profile.json`

## Setup

1. Create a GitHub repository and upload these files.
2. In GitHub, open **Settings → Secrets and variables → Actions**.
3. Add:
   - `GMAIL_ADDRESS`: the Gmail address that should send alerts
   - `GMAIL_APP_PASSWORD`: a Google App Password (never your normal Gmail password)
   - `ALERT_TO`: destination inbox (can be the same Gmail address)
4. Edit `config/profile.json` to verify your contact details, skills, education,
   location, and work authorisation. The provided profile is based on the resume
   supplied in this conversation; verify every field before enabling use.
5. Edit `config/boards.json` and add company Greenhouse board tokens or Lever
   site names. These feeds are public; board identifiers must be verified.
6. Run **Actions → Global Fresher Job Hunter → Run workflow** to test manually.
7. Enable the daily schedule after checking the first report.

## GitHub Actions schedule

The workflow runs daily at 03:30 UTC (09:00 India time). GitHub scheduled
workflows can be delayed during busy periods and may be disabled in inactive
public repositories.

## Scope and safety

- "Worldwide" means the discovery feeds can contain jobs in many countries;
  matching must still respect each listing's location and work-authorisation
  requirements.
- No minimum salary filter is applied.
- Job matching is a ranking aid, not a guarantee of eligibility.
- The starter records jobs as `discovered`; it never labels a job `applied`
  unless a supported adapter reports a confirmed submission.
- Add employer-specific application adapters only after checking their terms
  and implementing safeguards against duplicate submissions.
