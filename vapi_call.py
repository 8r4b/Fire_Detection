import requests

# ===============================
# CONFIGURATION
# ===============================

VAPI_API_KEY = "9b6e84c0-2db7-4ffa-9c80-d41378803cae"           # Replace with your VAPI API key
ASSISTANT_ID = "b525a65c-55d1-4599-9135-0333b2998bf8"          # Replace with your assistant ID
PHONE_NUMBER_ID = "610e9279-aae0-4962-b8c5-43176b56677a"  # Replace with the Twilio number ID imported into VAPI
DEST_NUMBER = "+9647736360937"              # Replace with your Iraqi number in E.164 format

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
