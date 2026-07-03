import json
import google.generativeai as genai
from config import API_KEY

# Configure Gemini
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    model = None


HIGH_RISK_PERMISSIONS = {
    "android.permission.READ_SMS": 15,
    "android.permission.RECEIVE_SMS": 15,
    "android.permission.SEND_SMS": 15,
    "android.permission.RECORD_AUDIO": 12,
    "android.permission.CAMERA": 10,
    "android.permission.READ_CONTACTS": 12,
    "android.permission.WRITE_CONTACTS": 10,
    "android.permission.ACCESS_FINE_LOCATION": 10,
    "android.permission.READ_CALL_LOG": 15,
    "android.permission.WRITE_CALL_LOG": 15,
    "android.permission.READ_PHONE_STATE": 8,
    "android.permission.REQUEST_INSTALL_PACKAGES": 15
}


def local_analysis(apk_data):

    permissions = apk_data.get("permissions", [])

    suspicious = []
    score = 0

    for permission in permissions:
        if permission in HIGH_RISK_PERMISSIONS:
            suspicious.append(permission)
            score += HIGH_RISK_PERMISSIONS[permission]

    score = min(score, 100)

    if score >= 80:
        severity = "Critical"
    elif score >= 60:
        severity = "High"
    elif score >= 30:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "risk_score": score,
        "severity": severity,
        "malware_family": "Unknown",
        "behavior_summary": (
            "Rule-based malware analysis completed successfully."
        ),
        "suspicious_permissions": suspicious,
        "possible_data_theft": (
            ["Contacts", "SMS", "Location"] if suspicious else []
        ),
        "possible_c2": "No evidence from static analysis",
        "mitre_attack": [
            "T1417",
            "T1430"
        ] if suspicious else [],
        "owasp_mobile": [
            "M2: Insecure Data Storage",
            "M4: Insecure Authentication"
        ] if suspicious else [],
        "recommendation": [
            "Scan with multiple antivirus engines.",
            "Run inside an Android sandbox.",
            "Review dangerous permissions before installation."
        ],
    }


def analyze_apk(apk_data):

    result = local_analysis(apk_data)

    if model is None:
        return result

    prompt = f"""
You are an Android malware analyst.

APK Metadata:

{json.dumps(apk_data, indent=2)}

Write ONLY one short paragraph summarizing the malware behaviour.
Do not return JSON.
"""

    try:
        response = model.generate_content(prompt)
        result["behavior_summary"] = response.text.strip()
    except Exception:
        # Ignore Gemini failures (quota, network, etc.)
        pass

    return result