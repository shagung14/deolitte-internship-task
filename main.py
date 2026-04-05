# This script converts two different telemetry JSON formats
# into a unified structure as defined in data-result.json
import json
from datetime import datetime

# Load JSON files
with open('data-1.json', encoding='utf-8') as f:
    data1 = json.load(f)

with open('data-2.json', encoding='utf-8') as f:
    data2 = json.load(f)


# Convert data-1.json → required format
def convert_data1(d):
    # Split location string into components
    parts = d["location"].split("/")

    return {
        "deviceID": d["deviceID"],
        "deviceType": d["deviceType"],
        "timestamp": d["timestamp"],  # already in milliseconds
        "location": {
            "country": parts[0],
            "city": parts[1],
            "area": parts[2],
            "factory": parts[3],
            "section": parts[4]
        },
        "data": {
            "status": d["operationStatus"],
            "temperature": d["temp"]
        }
    }


# Convert data-2.json → required format
def convert_data2(d):
    # Convert ISO timestamp to milliseconds since epoch
    dt = datetime.fromisoformat(d["timestamp"].replace("Z", "+00:00"))
    timestamp_ms = int(dt.timestamp() * 1000)

    return {
        "deviceID": d["device"]["id"],
        "deviceType": d["device"]["type"],
        "timestamp": timestamp_ms,
        "location": {
            "country": d["country"],
            "city": d["city"],
            "area": d["area"],
            "factory": d["factory"],
            "section": d["section"]
        },
        "data": {
            "status": d["data"]["status"],
            "temperature": d["data"]["temperature"]
        }
    }

# Convert both input datasets

# ✅ DO NOT USE LIST HERE
result1 = convert_data1(data1)
result2 = convert_data2(data2)


# Save output for format 1
with open('output-data1.json', 'w', encoding='utf-8') as f:
    json.dump(result1, f, indent=4, ensure_ascii=False)

# Save output for format 2
with open('output-data2.json', 'w', encoding='utf-8') as f:
    json.dump(result2, f, indent=4, ensure_ascii=False)

print("DONE! Files generated correctly")