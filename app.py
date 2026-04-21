import json
from flask import Flask, request, jsonify

app = Flask(__name__)

required_fields = ["id", "name", "email", "age", "country"]

@app.route("/transform", methods=["POST"])
def transform():
    try:
        data_from_x = request.get_json()

        if not data_from_x:
            return jsonify({
                "status": "error",
                "message": "No JSON data received"
            }), 400

        if isinstance(data_from_x, list):
            data_for_y = [
                {key: item.get(key) for key in required_fields}
                for item in data_from_x
            ]
        elif isinstance(data_from_x, dict):
            data_for_y = {
                key: data_from_x.get(key) for key in required_fields
            }
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON structure"
            }), 400

        return jsonify({
            "status": "success",
            "data": data_for_y
        })

    except Exception:
        return jsonify({
            "status": "error",
            "message": "Something went wrong"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)