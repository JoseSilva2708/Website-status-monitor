import json
import os
import time
import urllib.request
from urllib.request import URLError, HTTPError

WEBSITES = [ 
    "https://www.google.com",
    "https://github.com",
    "https://example.com",
]

def check_website(url:str, timeout: int=5) -> dict:
    start = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="GET")
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.status
            healthy = 200 <= status < 400
            error = None
    except HTTPError as e:
        status = e.code
        healthy = False
        error = str(e)
    except URLError as e:
        status = e.code
        healthy = False
        error = str(e.reason)
    except Exception as e:
        status = None
        healthy = False
        error = str(e)
        
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    
    return{
        "url": url,
        "status_code" : status,
        "healthy": healthy,
        "latency_ms": latency_ms,
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "error": error,
    }

def save_results(results, path="results.json"):
    history = []
    if os.path.exists(path):
        with open(path) as f:
            history = json.load(f)
    history.extend(results)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)
        
        
def should_alert(results):
    return [r for r in results if not r["healthy"]]
   
   
def lambda_handler(event, context):
    results = [check_website(url) for url in WEBSITES]
    down = should_alert(results)
    if down:
        print("ALERT: websites down:", down)
    
    save_results(results=results, path="results.json")
    return {"results": results}


if __name__ == "__main__":
    lambda_handler({}, {})
            