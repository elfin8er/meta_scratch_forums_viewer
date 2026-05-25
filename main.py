import feedparser
import json
from datetime import datetime, timezone
import inscriptis
import os
import scratchattach as sa
from dotenv import load_dotenv

load_dotenv()

def days_since_2000_utc(dt=datetime.now(timezone.utc)):
    epoch = datetime(2000, 1, 1, tzinfo=timezone.utc)
    delta = dt - epoch
    return delta.total_seconds() / 86400

with open("./src/project.json", "r") as file:
    project_data = json.load(file)

lists = project_data["targets"][0]["lists"]
variables = project_data["targets"][0]["variables"]

list_id_map = {
    "titles": "jh)T_=9*3$}bW$;W/eA~",
    "posts": "TdYg59v{KzJ[#0kv/]%=",
    "authors": "^*gK:o/OU5.Nr9+QK%fV",
    "topics": "!IJ^aKyel@myS0GotbI{",
    "post_time": "%MA`(e4?BTUK;gLyxf_D",
    "forum_ids": "fCcdlj+DO9v4bUc^YV~8",
    "forum_names": "AsY]2?/^WO;cS0fM{{?5"
}

variable_id_map = {
    "last_updated": "e|N6kLUX@W$|,_9N:CjW"
}

# Initialize all lists to empty
for list_id in list_id_map.values():
    lists[list_id][1] = []

# Update variables
variables[variable_id_map["last_updated"]][1] = days_since_2000_utc()

#FEED_URL = "https://scratch.mit.edu/discuss/feeds/forum/9"
FEED_BASE_URL = "https://scratch.mit.edu/discuss/feeds/forum/"
LIMIT = 14

lists[list_id_map["forum_ids"]] = ["forum_ids", [5, 6, 7, 8, 9, 10, 11, 60, 4, 1, 3, 31, 32]]

for forum_id in lists[list_id_map["forum_ids"]][1]:
    FEED_URL = f"{FEED_BASE_URL}{forum_id}"

    print("Fetching RSS feed...")
    feed = feedparser.parse(FEED_URL)

    if feed.bozo:
        print(f"Error fetching feed: {feed.bozo_exception}")
        exit(1)

    lists[list_id_map["forum_names"]][1].append(feed.entries[0].get("title").split(" :: ")[1])

    for entry in feed.entries[:LIMIT]:
        extracted_data = {
            "titles": entry.get("title").split(' :: ')[-1],
            "posts": inscriptis.get_text(entry.get("summary")),
            "authors": entry.get("author_detail", {}).get("name"),
            "topics": entry.get("link").split("/")[-2],
            "post_time": days_since_2000_utc(datetime.fromisoformat(entry.get("published")))
        }

        for key, value in extracted_data.items():
            lists[list_id_map[key]][1].append(value)

        # for key, list_id in list_id_map.items():
        #     lists[list_id].append(extracted_data[key])

with open("./src/project.json", "w") as file:
    json.dump(project_data, file, separators=(',', ':'))

# Connect to Scratch
session = sa.login(os.getenv("SCRATCH_USERNAME"), os.getenv("SCRATCH_PASSWORD"))
project = session.connect_project(os.getenv("SCRATCH_PROJECT_ID"))
project_name = f"Retro Scratch Forums [Updated: {datetime.now(timezone.utc).strftime('%m-%d @ %H:%M UTC')}]"
project.set_json(json.dumps(project_data, separators=(',', ':')))
project.set_title(project_name)