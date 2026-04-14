import requests
from collections import Counter
import concurrent.futures

URL = "http://13.235.128.118:8000/health"


def call_api():
    try:
        r = requests.get(URL)
        r.raise_for_status()
        return r.json().get("container_id", "MissingContainerId")
    except Exception:
        return "Failed"


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(lambda _: call_api(), range(100)))

print(Counter(results))
