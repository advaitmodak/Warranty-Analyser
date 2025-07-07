from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
import pandas as pd
from datetime import datetime
import os  # Needed for Render port binding

app = Flask(__name__)

# Load or create the Excel file
excel_file = "customer_complaints.xlsx"
try:
    df = pd.read_excel(excel_file, engine="openpyxl")
except FileNotFoundError:
    columns = [
        "Customer Name", "PO Number", "Product Failure Part Number",
        "Date of Supply", "Date of Commission", "Date of Failure",
        "Affected Quantity", "Description of Failure", "Pipeline Media",
        "Operating Pressure", "Operating Temperature", "Timestamp"
    ]
    df = pd.DataFrame(columns=columns)
    df.to_excel(excel_file, index=False, engine="openpyxl")

@app.route("/", methods=["GET"])
def home():
    return "Complaint Bot is running. Use /submit_complaint to POST data."

@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():
    data = request.json
    data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([data])
    updated_df = pd.concat([df, new_entry], ignore_index=True)
    updated_df.to_excel(excel_file, index=False, engine="openpyxl")
    return jsonify({"message": "Complaint submitted successfully."})

if __name__ == "__main__":
    # Bind to 0.0.0.0 and use PORT from environment (needed by Render)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
