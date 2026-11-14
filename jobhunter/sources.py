import requests

HEADERS = {"User-Agent": "GlobalFresherJobHunter/1.0 (personal job search)"}
TIMEOUT = 20

def fetch_greenhouse(token):
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    jobs = []
    for item in response.json().get("jobs", []):
        jobs.append({
            "source": "Greenhouse",
            "id": f"gh:{token}:{item.get('id')}",
            "title": item.get("title", ""),
            "company": token,
            "location": (item.get("location") or {}).get("name", ""),
            "url": item.get("absolute_url", ""),
            "description": item.get("content", "") or "",
            "updated_at": item.get("updated_at", "")
        })
    return jobs

def fetch_lever(site):
    url = f"https://api.lever.co/v0/postings/{site}?mode=json"
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    jobs = []
    for item in response.json():
        cats = item.get("categories") or {}
        jobs.append({
            "source": "Lever",
            "id": f"lever:{site}:{item.get('id')}",
            "title": item.get("text", ""),
            "company": site,
            "location": cats.get("location", ""),
            "url": item.get("hostedUrl", ""),
            "description": item.get("descriptionPlain", "") or "",
            "updated_at": item.get("createdAt", "")
        })
    return jobs
