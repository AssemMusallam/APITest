import json
import logging
import os
from flask import Flask, request, jsonify

# -------------------------------
# Configuration
# -------------------------------
API_KEY = os.getenv("API_KEY", "dev-key")  # use env variable in production
REQUIRED_FIELDS = ["id", "name", "email", "age", "country"]

# -------------------------------
# App Setup
# -------------------------------
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------------------
# Utility Functions
# -------------------------------
def check_api_key():
    key = request.headers.get("x-api-key")
    return key == API_KEY


def validate_input(data):
    if not data:
        return "No JSON data received"

    if not isinstance(data, (dict, list)):
        return "Invalid JSON structure (must be object or list)"

    return None


def transform_record(record):
    return {key: record.get(key) for key in REQUIRED_FIELDS}


# -------------------------------
# Routes
# -------------------------------
@app.route("/transform", methods=["POST"])
def transform():
    client_ip = request.remote_addr
    logging.info(f"Incoming request from {client_ip}")

    # 🔐 API Key Check
    if not check_api_key():
        logging.warning(f"Unauthorized access attempt from {client_ip}")
        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 401

    try:
        data_from_x = request.get_json()

        # ✅ Validation
        error = validate_input(data_from_x)
        if error:
            return jsonify({
                "status": "error",
                "message": error
            }), 400

        # 🔄 Transformation
        if isinstance(data_from_x, list):
            data_for_y = [transform_record(item) for item in data_from_x]
        else:
            data_for_y = transform_record(data_from_x)

        # 📤 Success Response
        return jsonify({
            "status": "success",
            "data": data_for_y
        }), 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running"
    }), 200


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
