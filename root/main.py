import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

# Fetch from environment
AUTH_USER = os.getenv("BASIC_AUTH_USER")
AUTH_PASS = os.getenv("BASIC_AUTH_PASS")

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not AUTH_USER or not AUTH_PASS:
        raise HTTPException(status_code=500, detail="Server misconfigured")
    valid_user = secrets.compare_digest(credentials.username, AUTH_USER)
    valid_pass = secrets.compare_digest(credentials.password, AUTH_PASS)
    if not (valid_user and valid_pass):
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/webhook")
async def webhook(request: Request, credentials: HTTPBasicCredentials = Depends(authenticate)):
    payload = await request.json()
    numeric_value = int(payload.get("Numeric_Value", 0))
    formatted = number_to_japanese_units(numeric_value)
    return {"formatted_value": formatted}

def number_to_japanese_units(n):
    if n < 1000:
        return str(n)
    elif n < 10000:
        return str(n)
    units = ["", "万", "億", "兆", "京"]
    num_str = str(n)
    result = []
    unit_index = 0
    while num_str:
        section = num_str[-4:]
        num_str = num_str[:-4]
        section_val = int(section)
        if section_val != 0:
            result.insert(0, str(section_val) + units[unit_index])
        unit_index += 1
    return "".join(result)
