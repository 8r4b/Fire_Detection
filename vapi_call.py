import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# CONFIGURATION
# ===============================

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
DEST_NUMBER = os.getenv("DEST_NUMBER")

VAPI_CALL_URL = "https://api.vapi.ai/call/phone"

# ===============================
# CREATE THE CALL
# ===============================

payload = {
    "assistantId": ASSISTANT_ID,
    "customer": {
        "number": DEST_NUMBER,
        "numberE164CheckEnabled": False
    },
    "phoneNumberId": PHONE_NUMBER_ID
}

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(VAPI_CALL_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()  # Raise exception if HTTP status is not 2xx

    data = response.json()
    print("Call successfully initiated!")
    print("Call info:", data)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} - {response.text}")
except requests.exceptions.RequestException as err:
    print(f"Request error: {err}")
