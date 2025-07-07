from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

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
    app.run(debug=True)
