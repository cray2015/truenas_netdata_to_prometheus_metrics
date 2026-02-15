import os
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import Response
import secrets

NETDATA_URL = "http://localhost:6999/api/v1/allmetrics?format=prometheus"

USERNAME = os.getenv("EXPORTER_USERNAME")
PASSWORD = os.getenv("EXPORTER_PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("EXPORTER_USERNAME and EXPORTER_PASSWORD must be set")

app = FastAPI()
security = HTTPBasic()

def verify(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, USERNAME)
    correct_pass = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/metrics")
def metrics(_: HTTPBasicCredentials = Depends(verify)):
    try:
        r = requests.get(NETDATA_URL, timeout=10)
        r.raise_for_status()
        return Response(content=r.text, media_type="text/plain")
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Failed to fetch Netdata metrics")