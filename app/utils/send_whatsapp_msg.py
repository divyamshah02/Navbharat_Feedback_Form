import requests
import json
import base64

def base64_to_text(b64_text):
    # Decode the Base64 string back to bytes, then to text
    return base64.b64decode(b64_text.encode()).decode()


INTERAKT_API_KEY = base64_to_text("TFV4V2VFbHNVakZmU1dkZk9VUklkRkZ0U0hoTlREQnlTemMxTkhVeFVGVldOalJJY2tkMFZFNWpSVG89")
BASE_URL = "https://api.interakt.ai/v1/public"


def send_interakt_message(api_key, phone_number, template_name, language_code, body_values=None, header_values=None, campaign_id=None, callback_data=None):
    """
    Send a WhatsApp template message via Interakt API.

    Parameters:
        api_key (str): Your Interakt API key.
        phone_number (str): Recipient phone number (without country code).
        template_name (str): Name of the approved WhatsApp template.
        language_code (str): Template language code (e.g., 'en', 'bg', etc.).
        body_values (list): List of values for template body variables.
        header_values (list): List of values for template header variables (e.g., media URLs).
        campaign_id (str, optional): Optional campaign ID.
        callback_data (str, optional): Any callback text or metadata.

    Returns:
        dict: API response JSON or error details.
    """

    url = "https://api.interakt.ai/v1/public/message/"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": phone_number,
        "callbackData": callback_data or "",
        "type": "Template",
        "template": {
            "name": template_name,
            "languageCode": language_code,
            "headerValues": header_values or [],            
            "bodyValues": body_values or []
        }
    }

    if campaign_id:
        payload["campaignId"] = campaign_id

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response.text)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"error - {e}")
        return {"success": False, "error": str(e)}


def send_interakt_button_message(api_key, phone_number, template_name, language_code, body_values=None, button_values=None, callback_data=None):
    """
    Send a WhatsApp Template message with button values via Interakt API.

    Parameters:
        api_key (str): Your Interakt API key.
        phone_number (str): Recipient phone number (without country code).
        template_name (str): Name of the approved WhatsApp template.
        language_code (str): Template language code (e.g., 'en').
        body_values (list): Values to substitute in the message body.
        button_values (dict): Button index to list of values, e.g., {"0": ["OTP123"]}.
        callback_data (str, optional): Optional callback text or metadata.

    Returns:
        dict: API response JSON or error details.
    """

    url = "https://api.interakt.ai/v1/public/message/"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": phone_number,
        "callbackData": callback_data or "",
        "type": "Template",
        "template": {
            "name": template_name,
            "languageCode": language_code,
            "bodyValues": body_values or [],
            "buttonValues": button_values or {}
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

