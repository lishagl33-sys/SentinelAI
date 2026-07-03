from flask import Flask, render_template, request, send_file
import os

from apk_parser import extract_apk_metadata
from gemini_service import analyze_apk
from pdf_generator import generate_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

latest_pdf = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    global latest_pdf

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

    # Analyze APK
    result = analyze_apk(apk_data)

    # Generate PDF
    latest_pdf = generate_pdf(result)

    return render_template(
        "result.html",
        result=result,
        metadata=apk_data
    )


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


if __name__ == "__main__":
    app.run(debug=True)