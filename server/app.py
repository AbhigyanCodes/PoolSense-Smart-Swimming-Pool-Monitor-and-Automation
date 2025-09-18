from flask import Flask, request, jsonify
import csv
from datetime import datetime
import os

app = Flask(__name__)
LOG_CSV = os.getenv("SERVER_LOG", "logs/server_data.csv")


def ensure_csv():
    """Ensure CSV file exists with header."""
    d = os.path.dirname(LOG_CSV)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "data"])


@app.route("/ingest", methods=["POST"])
def ingest():
    """Ingest JSON payload and append to CSV."""
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "invalid JSON"}), 400

    ensure_csv()
    with open(LOG_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), payload])

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
