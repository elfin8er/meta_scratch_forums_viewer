import feedparser
import re
import os
import json
from datetime import datetime, timezone

def format_time_ago(timestamp_str):
    # 1. Parse the ISO string into a timezone-aware datetime object
    # fromisoformat natively handles the '+00:00' suffix
    past_time = datetime.fromisoformat(timestamp_str)
    
    # 2. Get the current time in UTC so the timezones match perfectly
    now = datetime.now(timezone.utc)
    
    # 3. Calculate the total seconds between now and the post time
    diff = now - past_time
    seconds = int(diff.total_seconds())
    
    # Handle edge case where clock sync differences might show a negative number
    if seconds < 0:
        return "just now"
    
    # 4. Define our time thresholds in seconds
    intervals = (
        ('year', 31536000),   # 60 * 60 * 24 * 365
        ('month', 2592000),   # 60 * 60 * 24 * 30
        ('week', 604800),     # 60 * 60 * 24 * 7
        ('day', 86400),       # 60 * 60 * 24
        ('hour', 3600),       # 60 * 60
        ('minute', 60),
        ('second', 1)
    )
    
    # 5. Find the largest unit that fits
    for name, count in intervals:
        value = seconds // count
        if value >= 1:
            # Pluralize the unit name if the value is greater than 1
            unit = f"{name}s" if value > 1 else name
            return f"{value} {unit} ago"
            
    return "just now"

with open("./src/project.json", "r") as file:
    project_data = json.load(file)

FEED_URL = "https://scratch.mit.edu/discuss/feeds/forum/9"
print("Fetching RSS feed...")
feed = feedparser.parse(FEED_URL)

if feed.bozo:
    print(f"Error fetching feed: {feed.bozo_exception}")
    exit(1)

lists = project_data["targets"][0]["lists"]

id_map = {
    "1_title": "jh)T_=9*3$}bW$;W/eA~", # 1_titles
    "1_post": "TdYg59v{KzJ[#0kv/]%=", # 1_posts
    "1_author": "^*gK:o/OU5.Nr9+QK%fV", # 1_authors
    "1_id": "!IJ^aKyel@myS0GotbI{", # 1_topic
    "1_time_ago": "%MA`(e4?BTUK;gLyxf_D", # 1_post_time
    "2_title": "no-98aI?r[K8r7OU^sj2", # 2_titles
    "2_post": "1o(7Ld3RTKyYI-60zr+F", # 2_posts
    "2_author": "e*5hyOFd1C,Uh-t5Iirr", # 2_authors
    "2_id": "b.,MxzMXeT]N{w0KQbG", # 2_topic
    "2_time_ago": "En[dA4cU.TpX(lcqax@M", # 2_post_time
}

for list_id in id_map.values():
    lists[list_id][1] = []

for entry in feed.entries[:14]:
    extracted_data = {
        "1_title": entry.get("title").split(' :: ')[-1],
        "1_post": entry.get("summary"),
        "1_author": entry.get("author_detail", {}).get("name"),
        "1_id": entry.get("id").split("/")[-1],
        "1_time_ago": format_time_ago(entry.get("published"))
    }

    for key, list_id in id_map.items():
        lists[list_id][1].append(extracted_data[key])

with open("./project.json", "w") as file:
    json.dump(project_data, file, separators=(',', ':'))