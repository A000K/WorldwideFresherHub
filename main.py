import json
from pathlib import Path
from jobhunter.sources import fetch_greenhouse, fetch_lever
from jobhunter.matcher import score_job
from jobhunter.tracker import init_db, save_job, export_csv
from jobhunter.emailer import send_digest

def main():
    profile = json.loads(Path("config/profile.json").read_text())
    boards = json.loads(Path("config/boards.json").read_text())
    init_db()
    all_jobs = []
    errors = []

    for token in boards.get("greenhouse_board_tokens", []):
        try:
            all_jobs.extend(fetch_greenhouse(token))
        except Exception as exc:
            errors.append(f"Greenhouse {token}: {exc}")
    for site in boards.get("lever_site_names", []):
        try:
            all_jobs.extend(fetch_lever(site))
        except Exception as exc:
            errors.append(f"Lever {site}: {exc}")

    matches = []
    for job in all_jobs:
        score, reasons = score_job(job, profile)
        if score >= 20:
            save_job(job, score, reasons)
            matches.append((job, score, reasons))

    matches.sort(key=lambda x: x[1], reverse=True)
    export_csv()
    send_digest(matches)
    print(f"Fetched {len(all_jobs)} jobs; {len(matches)} keyword matches.")
    for err in errors:
        print("SOURCE ERROR:", err)

if __name__ == "__main__":
    main()
