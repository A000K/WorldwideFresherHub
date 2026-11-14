import sqlite3
from pathlib import Path
import csv

DB = Path("jobs.db")

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, source TEXT, company TEXT, title TEXT,
            location TEXT, url TEXT, score INTEGER, reasons TEXT,
            status TEXT DEFAULT 'discovered', first_seen TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

def save_job(job, score, reasons):
    with sqlite3.connect(DB) as con:
        con.execute("""INSERT OR IGNORE INTO jobs
        (id, source, company, title, location, url, score, reasons)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (job["id"], job["source"], job["company"], job["title"],
         job["location"], job["url"], score, "; ".join(reasons)))

def export_csv(path="jobs.csv"):
    with sqlite3.connect(DB) as con, open(path, "w", newline="", encoding="utf-8") as f:
        rows = con.execute("SELECT * FROM jobs ORDER BY score DESC, first_seen DESC").fetchall()
        writer = csv.writer(f)
        writer.writerow(["id","source","company","title","location","url","score",
                         "reasons","status","first_seen"])
        writer.writerows(rows)
