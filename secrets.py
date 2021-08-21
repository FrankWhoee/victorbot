import os
import json

secrets = None

# Extract secrets from local file.
if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        secrets = json.load(f)
else:
    secrets = {}
    secrets["token"] = os.environ.get("token")