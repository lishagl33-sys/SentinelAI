from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import os

from apk_parser import extract_apk_metadata
from gemini_service import analyze_apk
from pdf_generator import generate_pdf
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

latest_pdf = None
latest_result = None
HISTORY_FILE = "history.json"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    global latest_pdf
    global latest_result

    if "apk" not in request.files:
        return "No APK uploaded."

    file = request.files["apk"]

    if file.filename == "":
        return "Please select an APK."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract APK Metadata
    apk_data = extract_apk_metadata(filepath)
    apk_data["apk_size"] = round(os.path.getsize(filepath) / (1024 * 1024), 2)

    # Analyze APK
    result = analyze_apk(apk_data)
    latest_result = {
        "metadata": apk_data,
        "analysis": result
    }

    # Generate PDF
    latest_pdf = generate_pdf(result)
    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "app": apk_data.get("app_name"),
        "risk": result.get("risk_score"),
        "severity": result.get("severity")
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    return jsonify({
    "metadata": apk_data,
    "analysis": result
    })


@app.route("/download_pdf")
def download_pdf():

    global latest_pdf

    if latest_pdf and os.path.exists(latest_pdf):
        return send_file(
            latest_pdf,
            as_attachment=True,
            download_name="SentinelAI_Report.pdf"
        )

    return "PDF not found."



@app.route("/download_json")
def download_json():

    global latest_result

    if latest_result:
        return jsonify(latest_result)

    return jsonify({"error": "No analysis available"})


if __name__ == "__main__":
    app.run(debug=True)