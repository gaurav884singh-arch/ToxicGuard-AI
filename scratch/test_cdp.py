import subprocess
import time
import urllib.request
import json
import base64
import os

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proc = subprocess.Popen([
    EDGE_PATH,
    "--headless",
    "--disable-gpu",
    "--remote-debugging-port=9222"
])

try:
    time.sleep(2)
    # Check if debugging port responds
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/version")
    ver = json.loads(req.read().decode("utf-8"))
    print("CDP Version:", ver.get("Browser"))
finally:
    proc.terminate()
