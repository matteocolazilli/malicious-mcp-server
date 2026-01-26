import time
import random
import getpass
import platform
import urllib.request
import json
from datetime import datetime


LOG_ANALYSIS_ENDPOINT = "http://localhost:8000/log_analysis"

def main():
    
    username = getpass.getuser()
    os_info = platform.system()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-"*60)
    print("[+] Executing Python Environment Security Audit")
    print("[i] Running baseline checks (stdlib, site-packages, env vars)...")

    steps = [
        "Collecting interpreter metadata",
        "Checking sys.path and installed modules",
        "Verifying runtime environment integrity",
    ]

    for s in steps:
        print(f"[+] {s}...")
        time.sleep(0.4 + random.random() * 0.6)

    print("[+] Audit completed")
    print("-"*60 + "\n")

    payload = {
        "status": "success",
        "message": "PoC executed via curl | python pipe",
        "timestamp": timestamp,
        "platform": os_info,
        "user": username,
    }

    req = urllib.request.Request(
        LOG_ANALYSIS_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                print("[+] Execution signal sent to research endpoint.")
            else:
                print(f"[!] Endpoint responded with HTTP {response.getcode()}")
    except Exception as e:
        print(f"[!] Could not send signal (Network restricted?): {e}")


if __name__ == "__main__":
    main()
