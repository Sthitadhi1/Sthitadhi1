import os
import sys
import json
import re
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="Sthitadhi1", output_json="data/contributions.json"):
    # Append timestamp query parameter to bypass HTTP caching
    timestamp = int(time.time())
    url = f"https://github.com/users/{username}/contributions?timestamp={timestamp}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache"
    }

    days_data = []

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            
            day_elements = soup.select(".ContributionCalendar-day[data-date], rect[data-date]")
            print(f"Scraped {len(day_elements)} day elements from GitHub for user '{username}'.")
            
            tooltips = {}
            for tt in soup.find_all(["tool-tip", "div"], attrs={"for": True}):
                tooltips[tt["for"]] = tt.text.strip()
                
            for elem in day_elements:
                date = elem.get("data-date")
                if not date:
                    continue
                    
                level_str = elem.get("data-level", "0")
                try:
                    level = int(level_str)
                except ValueError:
                    level = 0
                    
                count = 0
                elem_id = elem.get("id")
                tooltip_text = tooltips.get(elem_id, "") or elem.get("aria-label", "") or ""
                
                if tooltip_text:
                    if "No contribution" in tooltip_text or "no contribution" in tooltip_text:
                        count = 0
                    else:
                        match = re.search(r"(\d+)\s+contribution", tooltip_text, re.IGNORECASE)
                        if match:
                            count = int(match.group(1))
                        elif level > 0:
                            count = level * 2
                elif level > 0:
                    count = level * 2

                days_data.append({
                    "date": date,
                    "count": count,
                    "level": level
                })
    except Exception as e:
        print(f"Warning: Failed to fetch online contributions for {username}: {e}")

    # Fallback if scraping failed to yield days
    if not days_data:
        print("Using cached contribution data...")
        if os.path.exists(output_json):
            with open(output_json, "r", encoding="utf-8") as f:
                cached = json.load(f)
                days_data = cached.get("days", [])

    if not days_data:
        today = datetime.now()
        start_date = today - timedelta(days=370)
        curr = start_date
        while curr <= today:
            days_data.append({
                "date": curr.strftime("%Y-%m-%d"),
                "count": 0,
                "level": 0
            })
            curr += timedelta(days=1)

    days_data.sort(key=lambda x: x["date"])

    total_contributions = sum(d["count"] for d in days_data)
    
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day_count = 0
    best_day_date = ""

    for d in days_data:
        cnt = d["count"]
        if cnt > best_day_count:
            best_day_count = cnt
            best_day_date = d["date"]
            
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    for d in reversed(days_data):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    result = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": best_day_date, "count": best_day_count},
        "days": days_data
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Successfully processed {len(days_data)} days for '{username}'. Total Contributions: {total_contributions}, Current Streak: {current_streak}, Longest Streak: {longest_streak}.")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "Sthitadhi1"
    fetch_contributions(uname)
