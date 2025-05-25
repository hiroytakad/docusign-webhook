from fastapi import FastAPI, Request
import requests

app = FastAPI()

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

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()

    numeric_value = int(payload.get("Numeric_Value", 0))
    object_id = payload.get("objectId", "N/A")

    formatted = number_to_japanese_units(numeric_value)

    print("Formatted:", formatted)
    return {"formatted_value": formatted}
